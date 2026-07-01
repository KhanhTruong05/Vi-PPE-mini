from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.run_judge import run_judge


def main() -> int:
    parser = argparse.ArgumentParser(description="Run judge inference over a pairwise dataset.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--backend", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--template", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--orders", nargs="+", default=["AB", "BA"], choices=["AB", "BA"])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    rows = run_judge(
        dataset_path=ROOT / args.dataset,
        template_name=args.template,
        run_id=args.run_id,
        backend_name=args.backend,
        model_name=args.model,
        orders=args.orders,
        resume=args.resume,
        limit=args.limit,
        output_path=ROOT / "results" / "judgments" / f"{args.run_id}.jsonl",
    )
    print(f"Wrote {len(rows)} new judgments to {ROOT / 'results' / 'judgments' / (args.run_id + '.jsonl')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
