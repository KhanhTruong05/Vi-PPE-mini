from collections import Counter

from vi_ppe.build_pairs import build_pairs
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import validate_pairs


def test_build_pairs_covers_three_domains():
    source_items = read_jsonl("data/interim/prompts_raw.jsonl")
    pairs = build_pairs(source_items, limit=90)
    validate_pairs(pairs)
    counts = Counter(pair["domain"] for pair in pairs)
    assert set(counts) == {"fact_check", "instruction", "safety"}
    assert all(count >= 20 for count in counts.values())


def test_pair_prompts_do_not_expose_gold_fields():
    source_items = read_jsonl("data/interim/prompts_raw.jsonl")
    pairs = build_pairs(source_items, limit=15)
    for pair in pairs:
        prompt = pair["prompt"].lower()
        assert "gold_winner" not in prompt
        assert "gold_reason" not in prompt
        assert pair["gold_winner"] in {"A", "B"}
