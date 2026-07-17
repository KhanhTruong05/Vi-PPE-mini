from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vi_ppe.io import read_jsonl


LABEL_COLUMNS = [
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
    "annotator_label",
    "annotator_reason",
]


def _load_pairs(paths: list[Path]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        for pair in read_jsonl(path):
            pair_id = pair["pair_id"]
            if pair_id in seen:
                continue
            seen.add(pair_id)
            pair = dict(pair)
            pair["source_split"] = "bias" if pair.get("diagnostic_subset") else "test"
            pairs.append(pair)
    return pairs


def _sample_balanced(pairs: list[dict[str, Any]], per_domain: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        by_domain[pair["domain"]].append(pair)

    selected: list[dict[str, Any]] = []
    for domain in sorted(by_domain):
        domain_pairs = list(by_domain[domain])
        rng.shuffle(domain_pairs)
        selected.extend(domain_pairs[:per_domain])

    selected.sort(key=lambda pair: (pair["domain"], pair["pair_id"]))
    return selected


def _write_sheet(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LABEL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def export_iaa_sample(
    input_paths: list[Path],
    output_dir: Path,
    per_domain: int,
    seed: int,
) -> dict[str, Any]:
    pairs = _load_pairs(input_paths)
    selected = _sample_balanced(pairs, per_domain=per_domain, seed=seed)

    rows: list[dict[str, str]] = []
    for pair in selected:
        rows.append(
            {
                "pair_id": pair["pair_id"],
                "source_split": pair.get("source_split", ""),
                "domain": pair["domain"],
                "prompt": pair["prompt"],
                "evidence": pair.get("evidence", ""),
                "response_a": pair["response_a"],
                "response_b": pair["response_b"],
                "criteria": "; ".join(pair.get("criteria", [])),
                "perturbation_type": pair.get("perturbation_type", ""),
                "source_dataset": pair.get("source_dataset", ""),
                "source_example_id": pair.get("source_example_id", ""),
                "annotator_label": "",
                "annotator_reason": "",
            }
        )

    sample_path = output_dir / "iaa_annotation_sample.csv"
    annotator_1_path = output_dir / "iaa_annotator_1.csv"
    annotator_2_path = output_dir / "iaa_annotator_2.csv"
    _write_sheet(sample_path, rows)
    _write_sheet(annotator_1_path, rows)
    _write_sheet(annotator_2_path, rows)

    return {
        "total_pairs_loaded": len(pairs),
        "sample_size": len(selected),
        "domain_counts": dict(Counter(pair["domain"] for pair in selected)),
        "source_split_counts": dict(Counter(pair.get("source_split", "") for pair in selected)),
        "sample_path": str(sample_path),
        "annotator_1_path": str(annotator_1_path),
        "annotator_2_path": str(annotator_2_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a balanced IAA annotation sample.")
    parser.add_argument(
        "--inputs",
        nargs="+",
        type=Path,
        default=[
            Path("data/processed/pairs_test_llm_v4.jsonl"),
            Path("data/processed/bias_subset_llm_v4.jsonl"),
        ],
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/iaa"))
    parser.add_argument("--per-domain", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260709)
    args = parser.parse_args()

    stats = export_iaa_sample(args.inputs, args.output_dir, args.per_domain, args.seed)
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
