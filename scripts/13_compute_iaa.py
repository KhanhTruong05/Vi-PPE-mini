from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


VALID_LABELS = {"A", "B", "tie"}

MERGED_COLUMNS = [
    "pair_id",
    "source_split",
    "domain",
    "prompt",
    "evidence",
    "response_a",
    "response_b",
    "criteria",
    "perturbation_type",
    "source_dataset",
    "source_example_id",
    "annotator_1_label",
    "annotator_1_reason",
    "annotator_2_label",
    "annotator_2_reason",
    "agreement_status",
    "adjudicated_gold_winner",
    "adjudicated_gold_reason",
]


def _read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return {row["pair_id"]: row for row in rows}


def _normalize_label(value: str) -> str:
    label = (value or "").strip()
    if label.lower() == "tie":
        return "tie"
    return label.upper()


def _cohen_kappa(label_pairs: list[tuple[str, str]]) -> float | None:
    if not label_pairs:
        return None
    total = len(label_pairs)
    observed = sum(1 for a, b in label_pairs if a == b) / total
    a_counts = Counter(a for a, _ in label_pairs)
    b_counts = Counter(b for _, b in label_pairs)
    expected = sum((a_counts[label] / total) * (b_counts[label] / total) for label in VALID_LABELS)
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)


def _agreement_stats(rows: list[dict[str, str]]) -> dict[str, Any]:
    valid_rows = [
        row
        for row in rows
        if row["annotator_1_label"] in VALID_LABELS and row["annotator_2_label"] in VALID_LABELS
    ]
    label_pairs = [(row["annotator_1_label"], row["annotator_2_label"]) for row in valid_rows]
    agreed = sum(1 for a, b in label_pairs if a == b)
    raw = agreed / len(valid_rows) if valid_rows else None
    return {
        "n": len(valid_rows),
        "raw_agreement": raw,
        "cohen_kappa": _cohen_kappa(label_pairs),
        "agreed": agreed,
        "disagreed": len(valid_rows) - agreed,
        "annotator_1_counts": dict(Counter(a for a, _ in label_pairs)),
        "annotator_2_counts": dict(Counter(b for _, b in label_pairs)),
    }


def merge_and_compute(annotator_1: Path, annotator_2: Path, output_csv: Path, report_md: Path) -> dict[str, Any]:
    rows_1 = _read_csv(annotator_1)
    rows_2 = _read_csv(annotator_2)
    pair_ids = sorted(set(rows_1) & set(rows_2))

    merged: list[dict[str, str]] = []
    invalid = Counter()
    for pair_id in pair_ids:
        row_1 = rows_1[pair_id]
        row_2 = rows_2[pair_id]
        label_1 = _normalize_label(row_1.get("annotator_label", ""))
        label_2 = _normalize_label(row_2.get("annotator_label", ""))
        if label_1 and label_1 not in VALID_LABELS:
            invalid["annotator_1_invalid"] += 1
        if label_2 and label_2 not in VALID_LABELS:
            invalid["annotator_2_invalid"] += 1

        status = ""
        if label_1 in VALID_LABELS and label_2 in VALID_LABELS:
            status = "agree" if label_1 == label_2 else "disagree"

        merged.append(
            {
                "pair_id": pair_id,
                "source_split": row_1.get("source_split", ""),
                "domain": row_1.get("domain", ""),
                "prompt": row_1.get("prompt", ""),
                "evidence": row_1.get("evidence", ""),
                "response_a": row_1.get("response_a", ""),
                "response_b": row_1.get("response_b", ""),
                "criteria": row_1.get("criteria", ""),
                "perturbation_type": row_1.get("perturbation_type", ""),
                "source_dataset": row_1.get("source_dataset", ""),
                "source_example_id": row_1.get("source_example_id", ""),
                "annotator_1_label": label_1,
                "annotator_1_reason": row_1.get("annotator_reason", ""),
                "annotator_2_label": label_2,
                "annotator_2_reason": row_2.get("annotator_reason", ""),
                "agreement_status": status,
                "adjudicated_gold_winner": "",
                "adjudicated_gold_reason": "",
            }
        )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MERGED_COLUMNS)
        writer.writeheader()
        writer.writerows(merged)

    overall = _agreement_stats(merged)
    by_domain: dict[str, dict[str, Any]] = {}
    domain_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in merged:
        domain_rows[row["domain"]].append(row)
    for domain, rows in sorted(domain_rows.items()):
        by_domain[domain] = _agreement_stats(rows)

    stats = {
        "total_rows_annotator_1": len(rows_1),
        "total_rows_annotator_2": len(rows_2),
        "matched_pair_ids": len(pair_ids),
        "missing_in_annotator_1": len(set(rows_2) - set(rows_1)),
        "missing_in_annotator_2": len(set(rows_1) - set(rows_2)),
        "invalid_labels": dict(invalid),
        "overall": overall,
        "by_domain": by_domain,
        "merged_csv": str(output_csv),
        "report_md": str(report_md),
    }

    _write_report(stats, report_md)
    return stats


def _format_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.2f}%"


def _format_float(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _write_report(stats: dict[str, Any], path: Path) -> None:
    overall = stats["overall"]
    lines = [
        "# IAA Report",
        "",
        "This report is computed from two independent annotator sheets. It does not modify frozen dataset labels or previous model results.",
        "",
        "## Overall",
        "",
        f"- Matched pairs: {stats['matched_pair_ids']}",
        f"- Valid double-labeled pairs: {overall['n']}",
        f"- Raw agreement: {_format_pct(overall['raw_agreement'])}",
        f"- Cohen's kappa: {_format_float(overall['cohen_kappa'])}",
        f"- Agreed pairs: {overall['agreed']}",
        f"- Disagreed pairs: {overall['disagreed']}",
        f"- Annotator 1 label counts: {overall['annotator_1_counts']}",
        f"- Annotator 2 label counts: {overall['annotator_2_counts']}",
        "",
        "## By Domain",
        "",
        "| Domain | Valid n | Raw agreement | Cohen's kappa | Agreed | Disagreed |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for domain, domain_stats in stats["by_domain"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    domain,
                    str(domain_stats["n"]),
                    _format_pct(domain_stats["raw_agreement"]),
                    _format_float(domain_stats["cohen_kappa"]),
                    str(domain_stats["agreed"]),
                    str(domain_stats["disagreed"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## QA",
            "",
            f"- Missing in annotator 1: {stats['missing_in_annotator_1']}",
            f"- Missing in annotator 2: {stats['missing_in_annotator_2']}",
            f"- Invalid labels: {stats['invalid_labels']}",
            "",
            "Rows with `agreement_status = disagree` should be adjudicated manually in the merged CSV.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge two IAA sheets and compute agreement.")
    parser.add_argument("--annotator-1", type=Path, default=Path("data/processed/iaa/iaa_annotator_1.csv"))
    parser.add_argument("--annotator-2", type=Path, default=Path("data/processed/iaa/iaa_annotator_2.csv"))
    parser.add_argument("--output-csv", type=Path, default=Path("data/processed/iaa/iaa_merged_with_adjudication.csv"))
    parser.add_argument("--report-md", type=Path, default=Path("reports/iaa_report.md"))
    args = parser.parse_args()

    stats = merge_and_compute(args.annotator_1, args.annotator_2, args.output_csv, args.report_md)
    print(f"matched_pair_ids: {stats['matched_pair_ids']}")
    print(f"valid_double_labeled_pairs: {stats['overall']['n']}")
    print(f"raw_agreement: {_format_pct(stats['overall']['raw_agreement'])}")
    print(f"cohen_kappa: {_format_float(stats['overall']['cohen_kappa'])}")
    print(f"merged_csv: {stats['merged_csv']}")
    print(f"report_md: {stats['report_md']}")


if __name__ == "__main__":
    main()
