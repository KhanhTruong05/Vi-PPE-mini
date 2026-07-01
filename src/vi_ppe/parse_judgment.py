from __future__ import annotations

import json
import re
from typing import Any

WINNER_ALIASES = {
    "a": "A",
    "response_a": "A",
    "answer_a": "A",
    "b": "B",
    "response_b": "B",
    "answer_b": "B",
    "tie": "tie",
    "draw": "tie",
    "equal": "tie",
}


def extract_first_json_object(raw_text: str) -> str | None:
    text = raw_text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if fenced:
        return fenced.group(1)
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def normalize_winner(value: Any) -> str:
    if value is None:
        return "invalid"
    return WINNER_ALIASES.get(str(value).strip().lower(), "invalid")


def parse_judgment(raw_text: str) -> dict[str, Any]:
    json_block = extract_first_json_object(raw_text)
    if not json_block:
        return {"parse_status": "failed", "winner": "invalid", "reason": "No JSON object found."}
    try:
        obj = json.loads(json_block)
    except json.JSONDecodeError as exc:
        return {"parse_status": "failed", "winner": "invalid", "reason": f"Invalid JSON: {exc}"}
    winner = normalize_winner(obj.get("winner"))
    if winner not in {"A", "B", "tie"}:
        return {"parse_status": "failed", "winner": "invalid", "raw_obj": obj}
    confidence = obj.get("confidence", 0.0)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0
    return {
        **obj,
        "winner": winner,
        "confidence": max(0.0, min(1.0, confidence)),
        "parse_status": "ok",
    }
