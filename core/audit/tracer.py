from __future__ import annotations

from core.models import BCell, LineageItem


def lineage_for(cells: list[BCell]) -> list[LineageItem]:
    return [
        LineageItem(
            cell_id=cell.id,
            domain=cell.domain,
            phase=cell.crystal_state.phase,
            trust_score=round(cell.trust_score, 4),
            reinforce_count=cell.crystal_state.reinforce_count,
            last_decay_t=cell.crystal_state.last_decay_t,
        )
        for cell in cells
    ]
