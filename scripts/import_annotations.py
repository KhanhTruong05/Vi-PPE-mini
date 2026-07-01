from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.annotation import import_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description="Import annotation CSV results into pair JSONL.")
    parser.add_argument("--annotations", required=True)
    parser.add_argument("--pairs", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    stats = import_annotations(ROOT / args.annotations, ROOT / args.pairs, ROOT / args.output)
    print(f"Wrote reviewed pairs to {ROOT / args.output}")
    print(f"Annotation stats: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
