from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.annotation import dataset_qa_report, write_qa_report
from vi_ppe.io import read_jsonl
from collections import Counter

from vi_ppe.schemas import validate_bias_pairs, validate_pairs, validate_source_items


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Vi-PPE-mini JSONL artifacts.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--type", choices=["pairs", "source_items"], default="pairs")
    parser.add_argument("--check-split", action="store_true", help="Reserved for Phase 6 split validation.")
    parser.add_argument("--require-bias-fields", action="store_true", help="Reserved for Phase 4 bias validation.")
    parser.add_argument("--qa-report", default=None, help="Reserved for Phase 5 QA report output.")
    args = parser.parse_args()

    records = read_jsonl(ROOT / args.input)
    if args.type == "source_items":
        validate_source_items(records)
    elif args.require_bias_fields:
        validate_bias_pairs(records)
        deltas = [record["length_a_tokens"] - record["length_b_tokens"] for record in records]
        buckets = Counter("A_longer" if d > 0 else "B_longer" if d < 0 else "same_length" for d in deltas)
        print(f"Delta length distribution: {dict(buckets)}")
    else:
        validate_pairs(records)
        if args.check_split:
            bad_status = [record["pair_id"] for record in records if record.get("review_status") == "needs_fix"]
            if bad_status:
                raise ValueError(f"Split contains needs_fix records: {bad_status[:10]}")
            draft_status = [record["pair_id"] for record in records if record.get("review_status") != "reviewed"]
            if draft_status:
                raise ValueError(f"Split contains non-reviewed records: {draft_status[:10]}")
            split_counts = Counter(record.get("split", "") for record in records)
            print(f"Split counts: {dict(split_counts)}")
    if args.qa_report:
        report = dataset_qa_report(records)
        write_qa_report(report, ROOT / args.qa_report)
        print(f"Wrote QA report to {ROOT / args.qa_report}")
    print(f"OK: validated {len(records)} {args.type} records from {args.input}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
