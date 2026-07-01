from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.metrics import compute_metrics
from vi_ppe.bias_metrics import write_bias_summary
from vi_ppe.io import read_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute swap aggregation and core metrics.")
    parser.add_argument("--judgments", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--bias", action="store_true", help="Compute bias diagnostics and write bias summary/figures.")
    args = parser.parse_args()
    metrics_dir = ROOT / "results" / "metrics"
    summary = compute_metrics(ROOT / args.judgments, ROOT / args.dataset, args.run_id, metrics_dir)
    if args.bias:
        pair_results = read_jsonl(metrics_dir / f"{args.run_id}_pair_results.jsonl")
        summary["bias_summary"] = write_bias_summary(pair_results, args.run_id, metrics_dir, ROOT / "results" / "figures")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
