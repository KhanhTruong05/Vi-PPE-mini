from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.schemas import WINNERS, count_tokens, validate_pairs

ANNOTATION_COLUMNS = [
    "pair_id",
    "domain",
    "prompt",
    "evidence",
    "response_a",
    "response_b",
    "draft_winner",
    "draft_reason",
    "reviewer_id",
    "annotator_winner",
    "annotator_reason",
    "needs_fix",
    "notes",
]


def export_annotation_sheet(
    input_path: str | Path,
    output_path: str | Path,
    sample: int | None = None,
    *,
    include_draft_labels: bool = False,
    prefill_annotations: bool = False,
) -> int:
    pairs = read_jsonl(input_path)
    selected = pairs[:sample] if sample is not None else pairs
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(output_path).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANNOTATION_COLUMNS)
        writer.writeheader()
        for pair in selected:
            writer.writerow(
                {
                    "pair_id": pair["pair_id"],
                    "domain": pair["domain"],
                    "prompt": pair["prompt"],
                    "evidence": pair.get("evidence", ""),
                    "response_a": pair["response_a"],
                    "response_b": pair["response_b"],
                    "draft_winner": pair["gold_winner"] if include_draft_labels else "",
                    "draft_reason": pair["gold_reason"] if include_draft_labels else "",
                    "reviewer_id": "",
                    "annotator_winner": pair["gold_winner"] if prefill_annotations else "",
                    "annotator_reason": pair["gold_reason"] if prefill_annotations else "",
                    "needs_fix": "",
                    "notes": "Human review required before this row can be marked reviewed.",
                }
            )
    return len(selected)


def _truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "x", "fix", "needs_fix"}


def import_annotations(annotations_path: str | Path, pairs_path: str | Path, output_path: str | Path) -> dict[str, int]:
    pairs = read_jsonl(pairs_path)
    by_id = {pair["pair_id"]: pair for pair in pairs}
    stats = Counter()

    with Path(annotations_path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pair_id = row.get("pair_id", "").strip()
            if pair_id not in by_id:
                stats["missing_pair_id"] += 1
                continue
            pair = by_id[pair_id]
            winner = (row.get("annotator_winner") or "").strip()
            reason = (row.get("annotator_reason") or "").strip()
            if _truthy(row.get("needs_fix", "")):
                pair["review_status"] = "needs_fix"
                stats["needs_fix"] += 1
                continue
            if not winner and not reason:
                stats["missing_annotation"] += 1
                continue
            if winner not in WINNERS:
                pair["review_status"] = "needs_fix"
                pair["metadata"] = {**pair.get("metadata", {}), "annotation_error": f"invalid winner {winner!r}"}
                stats["invalid_winner"] += 1
                continue
            if not reason:
                pair["review_status"] = "needs_fix"
                pair["metadata"] = {**pair.get("metadata", {}), "annotation_error": "missing annotator_reason"}
                stats["missing_reason"] += 1
                continue
            pair["gold_winner"] = winner
            pair["gold_reason"] = reason
            reviewer_id = (row.get("reviewer_id") or "human_annotation").strip()
            annotators = pair.get("annotators") or []
            if reviewer_id not in annotators:
                annotators.append(reviewer_id)
            pair["annotators"] = annotators
            pair["review_status"] = "reviewed"
            pair["metadata"] = {
                **pair.get("metadata", {}),
                "annotation_notes": row.get("notes", ""),
                "annotation_source": str(annotations_path),
            }
            stats["reviewed"] += 1

    write_jsonl(output_path, pairs)
    return dict(stats)


def dataset_qa_report(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    validate_pairs(pairs)
    prompt_to_ids: dict[str, list[str]] = defaultdict(list)
    response_to_ids: dict[str, list[str]] = defaultdict(list)
    length_mismatches = []
    missing_evidence_factcheck = []

    for pair in pairs:
        prompt_to_ids[pair["prompt"]].append(pair["pair_id"])
        response_to_ids[pair["response_a"]].append(f"{pair['pair_id']}:A")
        response_to_ids[pair["response_b"]].append(f"{pair['pair_id']}:B")
        if pair["domain"] == "fact_check" and not pair.get("evidence", "").strip():
            missing_evidence_factcheck.append(pair["pair_id"])
        if pair["length_a_tokens"] != count_tokens(pair["response_a"]) or pair["length_b_tokens"] != count_tokens(
            pair["response_b"]
        ):
            length_mismatches.append(pair["pair_id"])

    duplicate_prompts = {prompt: ids for prompt, ids in prompt_to_ids.items() if len(ids) > 1}
    duplicate_responses = {response: ids for response, ids in response_to_ids.items() if len(ids) > 1}
    return {
        "total_pairs": len(pairs),
        "domain_counts": dict(Counter(pair["domain"] for pair in pairs)),
        "perturbation_counts": dict(Counter(pair["perturbation_type"] for pair in pairs)),
        "review_status_counts": dict(Counter(pair["review_status"] for pair in pairs)),
        "gold_winner_counts": dict(Counter(pair["gold_winner"] for pair in pairs)),
        "needs_fix_ids": [pair["pair_id"] for pair in pairs if pair["review_status"] == "needs_fix"],
        "missing_evidence_factcheck": missing_evidence_factcheck,
        "length_mismatches": length_mismatches,
        "duplicate_prompt_count": len(duplicate_prompts),
        "duplicate_response_count": len(duplicate_responses),
    }


def write_qa_report(report: dict[str, Any], output_path: str | Path) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Dataset QA Report",
        "",
        f"- Total pairs: {report['total_pairs']}",
        f"- Domain counts: {report['domain_counts']}",
        f"- Perturbation counts: {report['perturbation_counts']}",
        f"- Review status counts: {report['review_status_counts']}",
        f"- Gold winner counts: {report['gold_winner_counts']}",
        f"- Needs fix count: {len(report['needs_fix_ids'])}",
        f"- Missing fact-check evidence count: {len(report['missing_evidence_factcheck'])}",
        f"- Length mismatch count: {len(report['length_mismatches'])}",
        f"- Duplicate prompt count: {report['duplicate_prompt_count']}",
        f"- Duplicate response count: {report['duplicate_response_count']}",
        "",
        "## Notes",
        "",
        "Rows marked reviewed require explicit annotator_winner and annotator_reason from the annotation sheet.",
    ]
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
