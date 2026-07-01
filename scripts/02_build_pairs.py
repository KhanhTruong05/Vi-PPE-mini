from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.bias_pair_builders import build_bias_subset, summarize_bias_pairs
from vi_ppe.build_pairs import build_pairs, summarize_pairs
from vi_ppe.io import read_jsonl, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Build draft pairwise examples from normalized source items.")
    parser.add_argument("--input", default="data/interim/prompts_raw.jsonl")
    parser.add_argument("--output", default="data/processed/pairs_all_draft.jsonl")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--bias-only", action="store_true", help="Reserved for Phase 4.")
    args = parser.parse_args()

    source_items = read_jsonl(ROOT / args.input)
    if args.bias_only:
        pairs = build_bias_subset(source_items, limit=args.limit)
        summary = summarize_bias_pairs(pairs)
    else:
        pairs = build_pairs(source_items, limit=args.limit)
        summary = summarize_pairs(pairs)
    write_jsonl(ROOT / args.output, pairs)
    print(f"Wrote {summary['total']} draft pairs to {ROOT / args.output}")
    print(f"Domain counts: {summary['domain_counts']}")
    print(f"Perturbation counts: {summary['perturbation_counts']}")
    if args.bias_only:
        print(f"Delta length min/max: {summary['delta_length_min']} / {summary['delta_length_max']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
