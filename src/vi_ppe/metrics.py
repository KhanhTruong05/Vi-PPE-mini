from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from vi_ppe.aggregate_swaps import aggregate_final_winner, map_to_original_space
from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.parse_judgment import parse_judgment


def normalize_judgment(judgment: dict[str, Any]) -> dict[str, Any]:
    raw_output = judgment.get("raw_output")
    if not isinstance(raw_output, str):
        return judgment
    reparsed = parse_judgment(raw_output)
    if reparsed.get("parse_status") != "ok":
        return judgment
    current = judgment.get("parsed", {})
    if current.get("parse_status") == "ok" and current.get("winner") == reparsed.get("winner"):
        return judgment
    return {
        **judgment,
        "parsed": reparsed,
        "parse_status": reparsed["parse_status"],
        "parse_recovered_at_metrics": True,
    }


def aggregate_judgments(judgments: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_pair = defaultdict(dict)
    for judgment in judgments:
        by_pair[judgment["pair_id"]][judgment["order"]] = judgment

    results = []
    for pair in pairs:
        rows = by_pair.get(pair["pair_id"], {})
        ab = rows.get("AB")
        ba = rows.get("BA")
        winner_ab = map_to_original_space(ab["parsed"]["winner"], "AB") if ab else "invalid"
        winner_ba = map_to_original_space(ba["parsed"]["winner"], "BA") if ba else "invalid"
        final, consistent = aggregate_final_winner(winner_ab, winner_ba)
        is_correct = final == pair["gold_winner"] if pair["gold_winner"] in {"A", "B"} else None
        chosen_longer = None
        delta_tokens = None
        if final in {"A", "B"}:
            chosen_len = pair["length_a_tokens"] if final == "A" else pair["length_b_tokens"]
            rejected_len = pair["length_b_tokens"] if final == "A" else pair["length_a_tokens"]
            chosen_longer = chosen_len > rejected_len
            delta_tokens = chosen_len - rejected_len
        results.append(
            {
                "pair_id": pair["pair_id"],
                "domain": pair["domain"],
                "perturbation_type": pair["perturbation_type"],
                "gold_winner": pair["gold_winner"],
                "winner_ab": winner_ab,
                "winner_ba_original_space": winner_ba,
                "final_winner": final,
                "is_correct": is_correct,
                "swap_consistent": consistent,
                "chosen_longer": chosen_longer,
                "delta_tokens_chosen_minus_rejected": delta_tokens,
                "length_a_tokens": pair["length_a_tokens"],
                "length_b_tokens": pair["length_b_tokens"],
                "style_a": pair.get("style_a"),
                "style_b": pair.get("style_b"),
                "prompt_template": ab["prompt_template"] if ab else None,
                "judge_model": ab["judge_model"] if ab else None,
                "has_ab": ab is not None,
                "has_ba": ba is not None,
            }
        )
    return results


def summarize(pair_results: list[dict[str, Any]], judgments: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in pair_results if row["gold_winner"] in {"A", "B"}]
    domain_accuracy = {}
    for domain in sorted({row["domain"] for row in eligible}):
        rows = [row for row in eligible if row["domain"] == domain]
        domain_accuracy[domain] = mean([row["is_correct"] for row in rows]) if rows else 0.0
    raw_ab = [j["parsed"]["winner"] for j in judgments if j["order"] == "AB" and j["parse_status"] == "ok"]
    raw_ba = [j["parsed"]["winner"] for j in judgments if j["order"] == "BA" and j["parse_status"] == "ok"]
    return {
        "num_pairs": len(pair_results),
        "num_judgments": len(judgments),
        "missing_ab_count": sum(not row["has_ab"] for row in pair_results),
        "missing_ba_count": sum(not row["has_ba"] for row in pair_results),
        "parse_success_rate": mean([j["parse_status"] == "ok" for j in judgments]) if judgments else 0.0,
        "pairwise_accuracy": mean([row["is_correct"] for row in eligible]) if eligible else 0.0,
        "domain_accuracy": domain_accuracy,
        "macro_accuracy": mean(domain_accuracy.values()) if domain_accuracy else 0.0,
        "lower_bound_domain_score": min(domain_accuracy.values()) if domain_accuracy else 0.0,
        "swap_consistency": mean([row["swap_consistent"] for row in pair_results]) if pair_results else 0.0,
        "inconsistent_count": sum(row["final_winner"] == "inconsistent" for row in pair_results),
        "invalid_count": sum(row["final_winner"] == "invalid" for row in pair_results),
        "final_winner_counts": dict(Counter(row["final_winner"] for row in pair_results)),
        "position_bias": {
            "raw_ab_winner_counts": dict(Counter(raw_ab)),
            "raw_ba_winner_counts": dict(Counter(raw_ba)),
        },
    }


def compute_metrics(
    judgments_path: str | Path,
    dataset_path: str | Path,
    run_id: str,
    output_dir: str | Path = "results/metrics",
    limit: int | None = None,
) -> dict[str, Any]:
    judgments = [normalize_judgment(row) for row in read_jsonl(judgments_path)]
    pairs = read_jsonl(dataset_path)
    if limit is not None:
        pairs = pairs[:limit]
        allowed_pair_ids = {pair["pair_id"] for pair in pairs}
        judgments = [row for row in judgments if row["pair_id"] in allowed_pair_ids]
    pair_results = aggregate_judgments(judgments, pairs)
    summary = summarize(pair_results, judgments)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    write_jsonl(output / f"{run_id}_pair_results.jsonl", pair_results)
    (output / f"{run_id}_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary
