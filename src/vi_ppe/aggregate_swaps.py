from __future__ import annotations


def map_to_original_space(winner: str, order: str) -> str:
    if winner not in {"A", "B", "tie"}:
        return "invalid"
    if winner == "tie":
        return "tie"
    if order == "AB":
        return winner
    if order == "BA":
        return {"A": "B", "B": "A"}[winner]
    return "invalid"


def aggregate_final_winner(winner_ab: str, winner_ba_original_space: str) -> tuple[str, bool]:
    if "invalid" in {winner_ab, winner_ba_original_space}:
        return "invalid", False
    if winner_ab == winner_ba_original_space:
        return winner_ab, True
    if "tie" in {winner_ab, winner_ba_original_space}:
        return winner_ba_original_space if winner_ab == "tie" else winner_ab, False
    return "inconsistent", False
