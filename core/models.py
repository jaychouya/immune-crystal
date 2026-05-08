from __future__ import annotations

import time
import uuid
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


Phase = Literal["stable", "reinforced", "quarantine", "purifying"]


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class CrystalState(BaseModel):
    phase: Phase = "stable"
    base_weight: float = 1.0
    amplitude: float = 0.35
    omega: float = 0.12
    phi: float = 0.0
    decay: float = 0.00005
    created_at: float = Field(default_factory=time.time)
    reinforce_count: int = 0
    last_decay_t: float = Field(default_factory=time.time)


class BCell(BaseModel):
    id: str = Field(default_factory=lambda: new_id("bc"))
    domain: str
    content: str
    source: str = "manual"
    compliance_tags: list[str] = Field(default_factory=list)
    trust_score: float = 0.8
    embedding: list[float] = Field(default_factory=list)
    crystal_state: CrystalState = Field(default_factory=CrystalState)
    access_series: list[float] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class Antibody(BaseModel):
    id: str = Field(default_factory=lambda: new_id("ab"))
    pattern: str
    domain: Optional[str] = None
    hits: int = 1
    created_at: float = Field(default_factory=time.time)


class DetectionResult(BaseModel):
    clean: bool
    pollution_prob: float
    reason: str
    matched_antibodies: list[str] = Field(default_factory=list)
    target_domain: Optional[str] = None


class LineageItem(BaseModel):
    cell_id: str
    domain: str
    phase: Phase
    trust_score: float
    reinforce_count: int
    last_decay_t: float


class AuditRecord(BaseModel):
    id: str = Field(default_factory=lambda: new_id("audit"))
    event: str
    query: Optional[str] = None
    answer: Optional[str] = None
    purity_score: Optional[float] = None
    lineage: list[LineageItem] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=time.time)


class ChatResult(BaseModel):
    answer: str
    purity: float
    lineage: list[LineageItem]
    audit_id: str
    blocked: bool = False
    reason: Optional[str] = None
