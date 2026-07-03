from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.llm_pair_generation import generate_pairs, load_env_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LLM-authored pairs in resumable chunks.")
    parser.add_argument("--input", default="data/interim/prompts_raw.jsonl")
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary-output", required=True)
    parser.add_argument("--mode", choices=["core", "bias"], default="core")
    parser.add_argument("--total", type=int, required=True)
    parser.add_argument("--chunk-size", type=int, default=30)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--budget-usd", type=float, default=5.0)
    parser.add_argument("--stop-cost-usd", type=float, default=4.75)
    parser.add_argument("--max-output-tokens", type=int, default=900)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--sleep-sec", type=float, default=0.05)
    parser.add_argument("--env-file", default=".env.local")
    args = parser.parse_args()

    load_env_file(ROOT / args.env_file)
    source_items = read_jsonl(ROOT / args.input)
    output_path = ROOT / args.output
    summary_path = ROOT / args.summary_output
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    while True:
        existing = read_jsonl(output_path) if output_path.exists() else []
        if len(existing) >= args.total:
            break
        next_total = min(args.total, len(existing) + args.chunk_size)
        records, summary = generate_pairs(
            source_items=source_items,
            mode=args.mode,
            total=next_total,
            model=args.model,
            budget_usd=args.budget_usd,
            stop_cost_usd=args.stop_cost_usd,
            max_output_tokens=args.max_output_tokens,
            temperature=args.temperature,
            retries=args.retries,
            sleep_sec=args.sleep_sec,
            existing_records=existing,
        )
        write_jsonl(output_path, records)
        summary["target_total"] = args.total
        summary["chunk_target"] = next_total
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False))

    final_records = read_jsonl(output_path)
    print(f"Done: {len(final_records)} records -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
