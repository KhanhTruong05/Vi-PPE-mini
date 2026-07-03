from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.annotation import export_annotation_sheet


def main() -> int:
    parser = argparse.ArgumentParser(description="Export pairwise examples to an annotation CSV.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument(
        "--include-draft-labels",
        action="store_true",
        help="Show generated draft labels for audit. Annotator fields remain blank.",
    )
    parser.add_argument(
        "--prefill-annotations",
        action="store_true",
        help="Legacy/bootstrap mode: copy generated labels into annotator fields.",
    )
    args = parser.parse_args()
    count = export_annotation_sheet(
        ROOT / args.input,
        ROOT / args.output,
        sample=args.sample,
        include_draft_labels=args.include_draft_labels,
        prefill_annotations=args.prefill_annotations,
    )
    print(f"Wrote {count} annotation rows to {ROOT / args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
