from vi_ppe.io import read_jsonl
from vi_ppe.prompt_render import choose_template, render_prompt


def test_baseline_prompt_has_no_gold_leakage():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    rendered = render_prompt(pair, "baseline_generic_vi", "AB")
    assert "gold_winner" not in rendered
    assert pair["gold_reason"] not in rendered
    assert "{{" not in rendered
    assert '"winner": "A" | "B" | "tie"' in rendered


def test_ba_order_swaps_responses():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    rendered_ab = render_prompt(pair, "baseline_generic_vi", "AB")
    rendered_ba = render_prompt(pair, "baseline_generic_vi", "BA")
    assert rendered_ab.index(pair["response_a"]) < rendered_ab.index(pair["response_b"])
    assert rendered_ba.index(pair["response_b"]) < rendered_ba.index(pair["response_a"])


def test_criteria_prompt_includes_rubric_and_bias_warning():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    rendered = render_prompt(pair, "criteria_fact_check_vi", "BA")
    assert "faithfulness_to_evidence" in rendered
    assert "Không thưởng cho câu trả lời dài hơn" in rendered
    assert "criteria_scores" in rendered


def test_auto_criteria_by_domain():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[4]
    assert choose_template(pair, "auto_criteria_by_domain") == "criteria_safety_vi"
    rendered = render_prompt(pair, "auto_criteria_by_domain", "AB")
    assert "harm_avoidance" in rendered
