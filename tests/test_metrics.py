from vi_ppe.aggregate_swaps import aggregate_final_winner, map_to_original_space
from vi_ppe.metrics import aggregate_judgments, summarize


def judgment(pair_id, order, winner):
    return {
        "pair_id": pair_id,
        "order": order,
        "parsed": {"winner": winner},
        "parse_status": "ok",
        "prompt_template": "baseline_generic_vi",
        "judge_model": "mock",
    }


def pair(pair_id, gold="A", domain="fact_check"):
    return {
        "pair_id": pair_id,
        "domain": domain,
        "perturbation_type": "test",
        "gold_winner": gold,
        "length_a_tokens": 5,
        "length_b_tokens": 10,
        "style_a": "plain",
        "style_b": "verbose",
    }


def test_map_ba_to_original_space():
    assert map_to_original_space("A", "BA") == "B"
    assert map_to_original_space("B", "BA") == "A"
    assert map_to_original_space("tie", "BA") == "tie"


def test_aggregate_final_winner_rules():
    assert aggregate_final_winner("A", "A") == ("A", True)
    assert aggregate_final_winner("tie", "B") == ("B", False)
    assert aggregate_final_winner("A", "B") == ("inconsistent", False)
    assert aggregate_final_winner("invalid", "invalid") == ("invalid", False)


def test_metrics_exclude_gold_tie_from_accuracy():
    pairs = [pair("p1", "A"), pair("p2", "tie", "instruction")]
    judgments = [
        judgment("p1", "AB", "A"),
        judgment("p1", "BA", "B"),
        judgment("p2", "AB", "A"),
        judgment("p2", "BA", "B"),
    ]
    rows = aggregate_judgments(judgments, pairs)
    summary = summarize(rows, judgments)
    assert summary["pairwise_accuracy"] == 1.0
    assert rows[1]["is_correct"] is None


def test_inconsistent_swap_reported_as_incorrect():
    pairs = [pair("p1", "A")]
    judgments = [judgment("p1", "AB", "A"), judgment("p1", "BA", "A")]
    rows = aggregate_judgments(judgments, pairs)
    summary = summarize(rows, judgments)
    assert rows[0]["final_winner"] == "inconsistent"
    assert rows[0]["is_correct"] is False
    assert summary["inconsistent_count"] == 1


def test_metrics_preserve_optional_style_tags():
    tagged_pair = {**pair("p1", "A"), "style_a_tag": "plain", "style_b_tag": "polished"}
    judgments = [judgment("p1", "AB", "A"), judgment("p1", "BA", "B")]
    rows = aggregate_judgments(judgments, [tagged_pair])
    assert rows[0]["style_a_tag"] == "plain"
    assert rows[0]["style_b_tag"] == "polished"
