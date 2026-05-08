from __future__ import annotations

from core.models import BCell


def purity_score(cells: list[BCell], similarities: list[float] | None = None) -> float:
    if not cells:
        return 0.0
    weights = similarities or [1.0] * len(cells)
    total = sum(max(0.0, w) for w in weights) or 1.0
    score = sum(cell.trust_score * max(0.0, weight) for cell, weight in zip(cells, weights)) / total
    quarantine_penalty = sum(0.08 for cell in cells if cell.crystal_state.phase == "quarantine")
    return round(max(0.0, min(1.0, score - quarantine_penalty)), 4)
