from __future__ import annotations

import math
import time

from core.models import BCell, CrystalState


class CrystalOscillator:
    def weight(self, state: CrystalState, at: float | None = None) -> float:
        now = at or time.time()
        age = max(0.0, now - state.created_at)
        wave = 1 + state.amplitude * math.cos(state.omega * age + state.phi)
        return max(0.0, state.base_weight * wave * math.exp(-state.decay * age))

    def score(self, cell: BCell, similarity: float, at: float | None = None) -> float:
        return similarity * self.weight(cell.crystal_state, at) * cell.trust_score

    def curve(self, cell: BCell, points: int = 64, step_seconds: int = 60) -> list[dict[str, float]]:
        start = time.time()
        return [
            {"t": i, "weight": self.weight(cell.crystal_state, start + i * step_seconds)}
            for i in range(points)
        ]

    def tick(self, cell: BCell) -> BCell:
        now = time.time()
        cell.access_series.append(self.weight(cell.crystal_state, now))
        cell.access_series = cell.access_series[-256:]
        if cell.crystal_state.phase == "purifying":
            cell.trust_score = max(0.0, cell.trust_score - 0.02)
        elif cell.crystal_state.phase == "reinforced":
            cell.trust_score = min(1.0, cell.trust_score + 0.01)
        cell.updated_at = now
        return cell
