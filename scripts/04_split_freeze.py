from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.config import load_project_config
from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.split_dataset import freeze_bias_subset, split_reviewed_pairs, write_dataset_card, write_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Split reviewed pairs and freeze dataset artifacts.")
    parser.add_argument("--input", default="data/processed/pairs_reviewed.jsonl")
    parser.add_argument("--bias", default="data/processed/bias_subset_reviewed.jsonl")
    parser.add_argument("--config", default="configs/project.yaml")
    parser.add_argument("--dev-output", default=None)
    parser.add_argument("--test-output", default=None)
    parser.add_argument("--bias-output", default=None)
    parser.add_argument("--manifest-output", default="data/processed/dataset_manifest.json")
    parser.add_argument("--card-output", default="reports/dataset_card.md")
    args = parser.parse_args()

    cfg = load_project_config(ROOT / args.config)
    seed = int(cfg["project"].get("seed", 42))
    dev_ratio = float(cfg["splits"].get("dev", 0.2))

    pairs = read_jsonl(ROOT / args.input)
    bias_pairs = read_jsonl(ROOT / args.bias)
    dev, test = split_reviewed_pairs(pairs, dev_ratio=dev_ratio, seed=seed)
    bias = freeze_bias_subset(bias_pairs)

    dev_path = ROOT / (args.dev_output or cfg["dataset"]["dev_pairs"])
    test_path = ROOT / (args.test_output or cfg["dataset"]["test_pairs"])
    bias_path = ROOT / (args.bias_output or cfg["dataset"]["bias_subset"])
    manifest_path = ROOT / args.manifest_output
    card_path = ROOT / args.card_output

    write_jsonl(dev_path, dev)
    write_jsonl(test_path, test)
    write_jsonl(bias_path, bias)
    write_manifest([dev_path, test_path, bias_path], manifest_path)
    write_dataset_card(output_path=card_path, dev=dev, test=test, bias=bias, manifest_path=manifest_path)

    print(f"Wrote dev split: {len(dev)} records -> {dev_path}")
    print(f"Wrote test split: {len(test)} records -> {test_path}")
    print(f"Wrote bias subset: {len(bias)} records -> {bias_path}")
    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote dataset card: {card_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
