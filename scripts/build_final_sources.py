from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.data_sources.vifactcheck import ViFactCheckAdapter
from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.schemas import validate_source_items


def main() -> int:
    parser = argparse.ArgumentParser(description="Build final local source items without network access.")
    parser.add_argument("--existing", default="data/interim/prompts_raw.jsonl")
    parser.add_argument("--vifactcheck-dir", default="data/raw/Vifactcheck_Dataset")
    parser.add_argument("--vifactcheck-limit", type=int, default=120)
    parser.add_argument("--output", default="data/interim/prompts_raw.jsonl")
    args = parser.parse_args()

    existing = read_jsonl(ROOT / args.existing)
    retained = [row for row in existing if row["source_dataset"] != "ViFactCheck"]
    vifact = ViFactCheckAdapter().iter_normalized(
        str(ROOT / args.vifactcheck_dir),
        limit=args.vifactcheck_limit,
    )
    records = vifact + retained
    validate_source_items(records)
    write_jsonl(ROOT / args.output, records)
    print(f"Wrote {len(records)} source items to {ROOT / args.output}")
    print(f"ViFactCheck items: {len(vifact)}")
    print(f"Retained non-ViFactCheck items: {len(retained)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
