from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

VERBOSITY_TYPES = {
    "concise_correct_vs_verbose_wrong",
    "same_content_different_length",
    "instruction_following_vs_over_elaboration",
    "appropriate_refusal_vs_verbose_moralizing",
}


def safe_mean(values: list[bool | float]) -> float | None:
    if not values:
        return None
    return float(mean(values))


def chosen_style(row: dict[str, Any]) -> str | None:
    if row["final_winner"] == "A":
        return row.get("style_a")
    if row["final_winner"] == "B":
        return row.get("style_b")
    return None


def verbosity_bias_rate(rows: list[dict[str, Any]]) -> float | None:
    controlled = [row for row in rows if row["perturbation_type"] in VERBOSITY_TYPES]
    choices = [row["chosen_longer"] for row in controlled if row.get("chosen_longer") is not None]
    return safe_mean(choices)


def style_bias_rate(rows: list[dict[str, Any]]) -> float | None:
    style_rows = [row for row in rows if row["perturbation_type"] == "plain_style_vs_polished_style"]
    choices = []
    for row in style_rows:
        style = chosen_style(row)
        if style is not None:
            choices.append(style == "polished")
    return safe_mean(choices)


def conditional_accuracy(rows: list[dict[str, Any]]) -> float | None:
    eligible = [row for row in rows if row["gold_winner"] in {"A", "B"} and row.get("is_correct") is not None]
    return safe_mean([row["is_correct"] for row in eligible])


def delta_length_distribution(rows: list[dict[str, Any]]) -> dict[str, int]:
    buckets = Counter()
    for row in rows:
        delta = row.get("delta_tokens_chosen_minus_rejected")
        if delta is None:
            buckets["no_choice"] += 1
        elif delta > 0:
            buckets["chosen_longer"] += 1
        elif delta < 0:
            buckets["chosen_shorter"] += 1
        else:
            buckets["same_length"] += 1
    return dict(buckets)


def length_delta_stats(rows: list[dict[str, Any]]) -> dict[str, int | None]:
    deltas = [row.get("delta_tokens_chosen_minus_rejected") for row in rows if row.get("delta_tokens_chosen_minus_rejected") is not None]
    if not deltas:
        return {"min": None, "max": None}
    return {"min": min(deltas), "max": max(deltas)}


def summarize_bias(rows: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    style_rows = [row for row in rows if row["perturbation_type"] == "plain_style_vs_polished_style"]
    verbosity_rows = [row for row in rows if row["perturbation_type"] in VERBOSITY_TYPES]
    return {
        "run_id": run_id,
        "num_pairs": len(rows),
        "conditional_accuracy": conditional_accuracy(rows),
        "verbosity_bias_rate": verbosity_bias_rate(rows),
        "style_bias_rate": style_bias_rate(rows),
        "swap_consistency_bias_subset": safe_mean([row["swap_consistent"] for row in rows]),
        "delta_length_distribution": delta_length_distribution(rows),
        "delta_tokens_chosen_minus_rejected": length_delta_stats(rows),
        "controlled_counts": {
            "verbosity_pairs": len(verbosity_rows),
            "style_pairs": len(style_rows),
        },
        "perturbation_counts": dict(Counter(row["perturbation_type"] for row in rows)),
        "note": "Bias should be interpreted jointly across accuracy, swap consistency, verbosity, style, and delta length distribution.",
    }


def write_bias_figures(rows: list[dict[str, Any]], run_id: str, output_dir: str | Path = "results/figures") -> list[str]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return []

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    figure_paths: list[str] = []

    summary = summarize_bias(rows, run_id)
    rates = {
        "conditional_accuracy": summary["conditional_accuracy"],
        "verbosity_bias_rate": summary["verbosity_bias_rate"],
        "style_bias_rate": summary["style_bias_rate"],
        "swap_consistency": summary["swap_consistency_bias_subset"],
    }
    available_rates = {name: value for name, value in rates.items() if value is not None}
    if available_rates:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(list(available_rates), list(available_rates.values()), color=["#3b82f6", "#ef4444", "#f59e0b", "#10b981"][: len(available_rates)])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Rate")
        ax.set_title(f"Bias diagnostics - {run_id}")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        path = output / f"{run_id}_bias_rates.png"
        fig.savefig(path, dpi=160)
        plt.close(fig)
        figure_paths.append(str(path))

    deltas = [row.get("delta_tokens_chosen_minus_rejected") for row in rows]
    indexed = [(idx, delta) for idx, delta in enumerate(deltas, start=1) if delta is not None]
    if indexed:
        xs, ys = zip(*indexed)
        colors = ["#ef4444" if delta > 0 else "#2563eb" if delta < 0 else "#64748b" for delta in ys]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(xs, ys, c=colors, s=18)
        ax.axhline(0, color="#111827", linewidth=1)
        ax.set_xlabel("Pair index")
        ax.set_ylabel("Delta tokens chosen - rejected")
        ax.set_title(f"Chosen length deltas - {run_id}")
        fig.tight_layout()
        path = output / f"{run_id}_delta_tokens_scatter.png"
        fig.savefig(path, dpi=160)
        plt.close(fig)
        figure_paths.append(str(path))

    return figure_paths


def write_bias_summary(
    rows: list[dict[str, Any]],
    run_id: str,
    output_dir: str | Path = "results/metrics",
    figures_dir: str | Path | None = None,
) -> dict[str, Any]:
    summary = summarize_bias(rows, run_id)
    if figures_dir is not None:
        summary["figure_paths"] = write_bias_figures(rows, run_id, figures_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{run_id}_bias_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary
