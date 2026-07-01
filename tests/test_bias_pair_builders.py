from vi_ppe.bias_pair_builders import build_bias_subset
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import validate_bias_pairs


def test_build_bias_subset_has_required_fields():
    source_items = read_jsonl("data/interim/prompts_raw.jsonl")
    pairs = build_bias_subset(source_items, limit=60)
    validate_bias_pairs(pairs)
    assert len(pairs) == 60
    assert all(pair["diagnostic_subset"] is True for pair in pairs)
    assert all(pair["bias_hypothesis"] for pair in pairs)


def test_bias_subset_contains_tie_pairs_for_non_core_accuracy():
    source_items = read_jsonl("data/interim/prompts_raw.jsonl")
    pairs = build_bias_subset(source_items, limit=60)
    assert any(pair["gold_winner"] == "tie" for pair in pairs)
