from __future__ import annotations

import time

from core.models import BCell


def reinforce(cell: BCell, amount: float = 0.04) -> BCell:
    cell.trust_score = min(1.0, cell.trust_score + amount)
    cell.crystal_state.phase = "reinforced"
    cell.crystal_state.reinforce_count += 1
    cell.crystal_state.last_decay_t = time.time()
    cell.updated_at = time.time()
    return cell
