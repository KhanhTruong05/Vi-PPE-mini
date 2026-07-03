from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.annotation import ANNOTATION_COLUMNS
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import WINNERS, count_tokens


def needs_fix_reason(pair: dict) -> str:
    if pair.get("gold_winner") not in WINNERS:
        return f"invalid generated winner {pair.get('gold_winner')!r}"
    if not pair.get("prompt", "").strip():
        return "empty prompt"
    if not pair.get("response_a", "").strip() or not pair.get("response_b", "").strip():
        return "empty response"
    if pair.get("response_a") == pair.get("response_b") and pair.get("gold_winner") != "tie":
        return "identical responses require tie or rewrite"
    if pair.get("domain") == "fact_check" and not pair.get("evidence", "").strip():
        return "fact_check pair missing evidence"
    if pair.get("length_a_tokens") != count_tokens(pair.get("response_a", "")):
        return "length_a_tokens mismatch"
    if pair.get("length_b_tokens") != count_tokens(pair.get("response_b", "")):
        return "length_b_tokens mismatch"
    if not pair.get("gold_reason", "").strip():
        return "missing generated reason"
    return ""


def build_row(pair: dict, *, include_draft_labels: bool) -> dict[str, str]:
    fix_reason = needs_fix_reason(pair)
    annotator_reason = ""
    if not fix_reason:
        annotator_reason = f"Codex-assisted review: {pair['gold_reason']}"
    return {
        "pair_id": pair["pair_id"],
        "domain": pair["domain"],
        "prompt": pair["prompt"],
        "evidence": pair.get("evidence", ""),
        "response_a": pair["response_a"],
        "response_b": pair["response_b"],
        "draft_winner": pair["gold_winner"] if include_draft_labels else "",
        "draft_reason": pair["gold_reason"] if include_draft_labels else "",
        "reviewer_id": "codex_assisted_review",
        "annotator_winner": "" if fix_reason else pair["gold_winner"],
        "annotator_reason": annotator_reason,
        "needs_fix": "1" if fix_reason else "",
        "notes": (
            f"Codex-assisted review marked needs_fix: {fix_reason}"
            if fix_reason
            else "Codex-assisted review accepted generated label; not human-reviewed."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Codex-assisted annotation CSV from draft pairs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--include-draft-labels", action="store_true")
    args = parser.parse_args()

    pairs = read_jsonl(ROOT / args.input)
    rows = [build_row(pair, include_draft_labels=args.include_draft_labels) for pair in pairs]
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANNOTATION_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    needs_fix_count = sum(1 for row in rows if row["needs_fix"])
    reviewed_count = len(rows) - needs_fix_count
    print(f"Wrote {len(rows)} Codex-assisted review rows to {output}")
    print(f"Reviewed rows: {reviewed_count}")
    print(f"Needs-fix rows: {needs_fix_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
