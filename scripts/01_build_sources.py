from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.config import load_project_config
from vi_ppe.data_sources import build_adapter
from vi_ppe.io import write_jsonl
from vi_ppe.schemas import validate_source_items


def build_sources(config_path: str, limit_per_source: int | None = None, output: str | None = None) -> list[dict]:
    cfg = load_project_config(ROOT / config_path)
    output_path = ROOT / (output or cfg["dataset"]["prompts_raw"])
    records = []
    warnings = []

    for source_cfg in cfg.get("sources", []):
        if source_cfg.get("enabled", True) is False:
            continue
        name = source_cfg["name"]
        path = source_cfg.get("path")
        hf_id = source_cfg.get("hf_id")
        split = source_cfg.get("split")
        adapter = build_adapter(name)
        local_path = ROOT / path if path else None
        if local_path and local_path.exists():
            input_ref = str(local_path)
        elif hf_id:
            input_ref = hf_id
        elif path:
            input_ref = str(local_path)
        else:
            input_ref = None
        source_records = adapter.iter_normalized(input_ref, limit=limit_per_source, split=split)
        for item in source_records:
            if item["license_note"].strip().lower() == "unknown":
                warnings.append(f"WARNING: {item['source_example_id']} has unknown license_note")
        records.extend(source_records)
        print(f"Loaded {len(source_records)} source items from {name}")

    validate_source_items(records)
    write_jsonl(output_path, records)
    print(f"Wrote {len(records)} source items to {output_path}")
    for warning in warnings:
        print(warning)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Build normalized source items.")
    parser.add_argument("--config", default="configs/project.yaml")
    parser.add_argument("--limit-per-source", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    build_sources(args.config, args.limit_per_source, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
