import pytest

from vi_ppe.config import load_project_config
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import (
    CRITERION_DESCRIPTIONS,
    DOMAIN_CRITERIA,
    SchemaError,
    criteria_for_domain,
    is_core_accuracy_pair,
    validate_pair,
    validate_pairs,
    validate_rubric_config,
)


def test_smoke_pairs_are_valid():
    pairs = read_jsonl("data/samples/smoke_pairs.jsonl")
    validate_pairs(pairs)


def test_missing_required_field_fails():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    pair.pop("gold_reason")
    with pytest.raises(SchemaError, match="missing fields"):
        validate_pair(pair)


def test_invalid_domain_criterion_fails():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    pair["criteria"] = ["format_correctness"]
    with pytest.raises(SchemaError, match="not valid for domain"):
        validate_pair(pair)


def test_project_rubric_config_matches_schema():
    cfg = load_project_config("configs/project.yaml")
    validate_rubric_config(cfg["rubrics"])


def test_each_domain_has_five_documented_criteria():
    for domain, criteria in DOMAIN_CRITERIA.items():
        assert len(criteria) == 5, domain
        assert criteria_for_domain(domain) == criteria
        for criterion in criteria:
            assert criterion in CRITERION_DESCRIPTIONS
            assert CRITERION_DESCRIPTIONS[criterion]


def test_tie_is_valid_but_excluded_from_core_accuracy():
    pair = read_jsonl("data/samples/smoke_pairs.jsonl")[0]
    pair["gold_winner"] = "tie"
    pair["gold_reason"] = "Both answers are equivalent under the rubric."
    validate_pair(pair)
    assert is_core_accuracy_pair(pair) is False
