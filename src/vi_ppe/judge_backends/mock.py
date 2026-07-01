from __future__ import annotations

import json


class MockJudgeBackend:
    judge_model = "mock"

    def generate(self, prompt: str, pair: dict, order: str) -> str:
        winner = pair["gold_winner"]
        if order == "BA":
            if winner == "A":
                winner = "B"
            elif winner == "B":
                winner = "A"
        payload = {
            "winner": winner,
            "confidence": 0.99,
            "reason": "Mock backend follows the gold label for pipeline smoke testing.",
        }
        return json.dumps(payload, ensure_ascii=False)
