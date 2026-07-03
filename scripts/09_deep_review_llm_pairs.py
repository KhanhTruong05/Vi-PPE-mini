from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.annotation import ANNOTATION_COLUMNS
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import WINNERS, count_tokens

ARTIFACT_PATTERNS = [
    "better_response",
    "worse_response",
    "draft_reason",
    "prompt_seed",
    "source item",
    "json object",
    "llm-as-a-judge",
]

ENGLISH_VERDICT_LABELS = ["SUPPORTED", "REFUTED", "NEI"]
INSTRUCTION_FORBIDDEN = ["prompt_seed", "better_response", "worse_response"]


def contains_any(text: str, patterns: list[str]) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in patterns if pattern.lower() in lowered]


def quality_issues(pair: dict) -> list[str]:
    issues: list[str] = []
    pair_id = pair.get("pair_id", "<unknown>")
    domain = pair.get("domain", "")
    prompt = str(pair.get("prompt", ""))
    response_a = str(pair.get("response_a", ""))
    response_b = str(pair.get("response_b", ""))
    reason = str(pair.get("gold_reason", ""))

    if pair.get("gold_winner") not in WINNERS:
        issues.append(f"{pair_id}: invalid gold_winner")
    if not prompt.strip():
        issues.append(f"{pair_id}: empty prompt")
    if not response_a.strip() or not response_b.strip():
        issues.append(f"{pair_id}: empty response")
    if response_a.strip() == response_b.strip() and pair.get("gold_winner") != "tie":
        issues.append(f"{pair_id}: identical responses but non-tie winner")
    if not reason.strip():
        issues.append(f"{pair_id}: empty draft reason")
    if pair.get("length_a_tokens") != count_tokens(response_a):
        issues.append(f"{pair_id}: length_a_tokens mismatch")
    if pair.get("length_b_tokens") != count_tokens(response_b):
        issues.append(f"{pair_id}: length_b_tokens mismatch")

    artifact_hits = contains_any("\n".join([prompt, response_a, response_b]), ARTIFACT_PATTERNS)
    if artifact_hits:
        issues.append(f"{pair_id}: visible generation artifact(s): {', '.join(artifact_hits)}")

    if domain == "fact_check":
        if not str(pair.get("evidence", "")).strip():
            issues.append(f"{pair_id}: fact_check missing evidence")
        verdict_hits = [label for label in ENGLISH_VERDICT_LABELS if label in response_a or label in response_b]
        if verdict_hits:
            issues.append(f"{pair_id}: response uses English verdict label(s): {', '.join(verdict_hits)}")
    elif domain == "instruction":
        forbidden_hits = contains_any(prompt, INSTRUCTION_FORBIDDEN)
        if forbidden_hits:
            issues.append(f"{pair_id}: instruction prompt includes fact-check wording: {', '.join(forbidden_hits)}")
    elif domain == "safety":
        if "xin nghỉ phép" in prompt.lower() or "json" in prompt.lower():
            issues.append(f"{pair_id}: safety prompt appears to be instruction task")

    return issues


def rewrite_reason(pair: dict) -> str:
    winner = pair["gold_winner"]
    reason = str(pair.get("gold_reason", "")).strip()
    if winner == "A":
        reason = reason.replace("Better_response", "A").replace("better_response", "A")
        reason = reason.replace("Worse_response", "B").replace("worse_response", "B")
    elif winner == "B":
        reason = reason.replace("Better_response", "B").replace("better_response", "B")
        reason = reason.replace("Worse_response", "A").replace("worse_response", "A")
    else:
        reason = reason.replace("Better_response", "một phản hồi").replace("better_response", "một phản hồi")
        reason = reason.replace("Worse_response", "phản hồi còn lại").replace("worse_response", "phản hồi còn lại")
    reason = reason.replace("LLM draft label:", "").strip()
    if not reason:
        reason = "Codex-assisted deep review: nhãn draft hợp lý theo rubric; cần human audit nếu dùng cho claim cuối."
    if not reason.lower().startswith("codex-assisted deep review"):
        reason = f"Codex-assisted deep review: {reason}"
    return reason


def build_review_row(pair: dict, *, include_draft_labels: bool) -> dict[str, str]:
    issues = quality_issues(pair)
    if issues:
        winner = ""
        reason = ""
        needs_fix = "1"
        notes = " | ".join(issues)
    else:
        winner = pair["gold_winner"]
        reason = rewrite_reason(pair)
        needs_fix = ""
        notes = "Codex-assisted deep review accepted draft label after quality checks; not human-reviewed."
    return {
        "pair_id": pair["pair_id"],
        "domain": pair["domain"],
        "prompt": pair["prompt"],
        "evidence": pair.get("evidence", ""),
        "response_a": pair["response_a"],
        "response_b": pair["response_b"],
        "draft_winner": pair["gold_winner"] if include_draft_labels else "",
        "draft_reason": pair["gold_reason"] if include_draft_labels else "",
        "reviewer_id": "codex_assisted_deep_review",
        "annotator_winner": winner,
        "annotator_reason": reason,
        "needs_fix": needs_fix,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deep Codex-assisted review for LLM-generated draft pairs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--include-draft-labels", action="store_true")
    args = parser.parse_args()

    pairs = read_jsonl(ROOT / args.input)
    rows = [build_review_row(pair, include_draft_labels=args.include_draft_labels) for pair in pairs]
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANNOTATION_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    needs_fix_count = sum(1 for row in rows if row["needs_fix"])
    print(f"Wrote {len(rows)} review rows to {output}")
    print(f"Accepted rows: {len(rows) - needs_fix_count}")
    print(f"Needs-fix rows: {needs_fix_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
