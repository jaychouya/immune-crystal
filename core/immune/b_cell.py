from __future__ import annotations

from core.models import BCell, CrystalState


def create_b_cell(
    content: str,
    domain: str,
    source: str = "manual",
    compliance_tags: list[str] | None = None,
    trust_score: float = 0.82,
) -> BCell:
    compliance_boost = min(0.2, 0.04 * len(compliance_tags or []))
    state = CrystalState(amplitude=0.3 + compliance_boost)
    return BCell(
        domain=domain,
        content=content,
        source=source,
        compliance_tags=compliance_tags or [],
        trust_score=trust_score,
        crystal_state=state,
    )
