from __future__ import annotations

import time

from core.models import BCell


def decay(cell: BCell, amount: float = 0.03) -> BCell:
    cell.trust_score = max(0.0, cell.trust_score - amount)
    cell.crystal_state.last_decay_t = time.time()
    if cell.trust_score < 0.35:
        cell.crystal_state.phase = "quarantine"
    cell.updated_at = time.time()
    return cell
