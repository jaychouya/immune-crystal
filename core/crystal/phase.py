from __future__ import annotations

import time

from core.models import BCell


def split_conflict(left: BCell, right: BCell, delta: float = 0.06) -> tuple[BCell, BCell]:
    left.crystal_state.omega += delta
    right.crystal_state.omega = max(0.01, right.crystal_state.omega - delta)
    left.crystal_state.phase = "quarantine"
    right.crystal_state.phase = "quarantine"
    left.trust_score *= 0.75
    right.trust_score *= 0.75
    now = time.time()
    left.updated_at = now
    right.updated_at = now
    return left, right


def quarantine_conflict(cell: BCell, delta: float = 0.06) -> BCell:
    cell.crystal_state.omega += delta
    cell.crystal_state.phase = "quarantine"
    cell.trust_score *= 0.75
    cell.updated_at = time.time()
    return cell


def reset_to_purifying(cell: BCell) -> BCell:
    cell.crystal_state.phase = "purifying"
    cell.crystal_state.amplitude = 0.05
    cell.crystal_state.base_weight *= 0.5
    cell.trust_score = min(cell.trust_score, 0.4)
    cell.updated_at = time.time()
    return cell


def stabilize(cell: BCell) -> BCell:
    cell.crystal_state.phase = "stable"
    cell.crystal_state.amplitude = max(cell.crystal_state.amplitude, 0.2)
    cell.updated_at = time.time()
    return cell
