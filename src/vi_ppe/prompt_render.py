from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, "", "src.vi_ppe"}:
    src_path = Path(__file__).resolve().parents[1]
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

from vi_ppe.io import read_jsonl
from vi_ppe.schemas import CRITERION_DESCRIPTIONS, DOMAIN_CRITERIA

ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = ROOT / "prompts"

AUTO_CRITERIA_TEMPLATES = {
    "fact_check": "criteria_fact_check_vi",
    "instruction": "criteria_instruction_vi",
    "safety": "criteria_safety_vi",
}


def template_path(template_name: str) -> Path:
    name = template_name[:-3] if template_name.endswith(".md") else template_name
    return PROMPT_DIR / f"{name}.md"


def load_prompt_template(template_name: str) -> str:
    path = template_path(template_name)
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8")


def choose_template(pair: dict[str, Any], template_name: str) -> str:
    if template_name in {"auto_criteria_by_domain", "criteria_auto"}:
        return AUTO_CRITERIA_TEMPLATES[pair["domain"]]
    return template_name


def render_criteria(domain: str) -> str:
    criteria = sorted(DOMAIN_CRITERIA[domain])
    return "\n".join(f"- `{criterion}`: {CRITERION_DESCRIPTIONS[criterion]}" for criterion in criteria)


def pair_for_order(pair: dict[str, Any], order: str) -> tuple[str, str]:
    if order == "AB":
        return pair["response_a"], pair["response_b"]
    if order == "BA":
        return pair["response_b"], pair["response_a"]
    raise ValueError("order must be AB or BA")


def render_prompt(pair: dict[str, Any], template_name: str, order: str = "AB") -> str:
    actual_template = choose_template(pair, template_name)
    template = load_prompt_template(actual_template)
    response_a, response_b = pair_for_order(pair, order)
    values = {
        "domain": pair["domain"],
        "prompt": pair["prompt"],
        "evidence": pair.get("evidence") or "Không có",
        "response_a": response_a,
        "response_b": response_b,
        "criteria_block": render_criteria(pair["domain"]),
    }
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"Unresolved placeholder in template {actual_template}")
    if "gold_winner" in rendered or "gold_reason" in rendered:
        raise ValueError("Rendered prompt leaks gold field names")
    gold_reason = pair.get("gold_reason", "")
    if gold_reason and gold_reason in rendered:
        raise ValueError("Rendered prompt leaks gold reason")
    return rendered


def load_pair(dataset_path: str | Path, pair_id: str) -> dict[str, Any]:
    for pair in read_jsonl(dataset_path):
        if pair["pair_id"] == pair_id:
            return pair
    raise KeyError(f"Pair id not found: {pair_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a judge prompt for a pair.")
    parser.add_argument("--pair-id", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--order", choices=["AB", "BA"], default="AB")
    args = parser.parse_args()

    pair = load_pair(Path(args.dataset), args.pair_id)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(render_prompt(pair, args.template, args.order))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
