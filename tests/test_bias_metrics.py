from vi_ppe.bias_metrics import (
    conditional_accuracy,
    delta_length_distribution,
    style_bias_rate,
    summarize_bias,
    verbosity_bias_rate,
)


def row(**kwargs):
    base = {
        "run_id": "r",
        "perturbation_type": "concise_correct_vs_verbose_wrong",
        "gold_winner": "A",
        "is_correct": True,
        "final_winner": "A",
        "chosen_longer": False,
        "delta_tokens_chosen_minus_rejected": -10,
        "style_a": "plain",
        "style_b": "verbose",
        "swap_consistent": True,
    }
    base.update(kwargs)
    return base


def test_verbosity_bias_rate_uses_controlled_types():
    rows = [row(chosen_longer=True), row(chosen_longer=False), row(perturbation_type="plain_style_vs_polished_style", chosen_longer=True)]
    assert verbosity_bias_rate(rows) == 0.5


def test_style_bias_rate_tracks_polished_choice():
    rows = [
        row(perturbation_type="plain_style_vs_polished_style", final_winner="B", style_b="polished"),
        row(perturbation_type="plain_style_vs_polished_style", final_winner="A", style_a="plain"),
    ]
    assert style_bias_rate(rows) == 0.5


def test_conditional_accuracy_excludes_tie_gold():
    rows = [row(is_correct=True), row(gold_winner="tie", is_correct=None), row(is_correct=False)]
    assert conditional_accuracy(rows) == 0.5


def test_bias_summary_contains_delta_distribution():
    rows = [row(delta_tokens_chosen_minus_rejected=2), row(delta_tokens_chosen_minus_rejected=-1), row(delta_tokens_chosen_minus_rejected=None)]
    summary = summarize_bias(rows, "r")
    assert summary["delta_length_distribution"] == {"chosen_longer": 1, "chosen_shorter": 1, "no_choice": 1}
    assert "verbosity_bias_rate" in summary
