from __future__ import annotations

import os

from core.audit import AuditLogger, lineage_for, purity_score
from core.crystal import CrystalOscillator
from core.crystal.phase import quarantine_conflict, reset_to_purifying
from core.detector import ConflictDetector
from core.domain import DomainRegistry
from core.immune import TCell, create_b_cell
from core.llm import QwenLocal, StubLLM
from core.memory.reinforcer import reinforce
from core.memory.store import MemoryStore
from core.models import AuditRecord, BCell, ChatResult


class ImmuneCrystal:
    def __init__(self) -> None:
        self.store = MemoryStore()
        self.audit = AuditLogger()
        self.domains = DomainRegistry()
        self.t_cell = TCell(registry=self.domains)
        self.conflicts = ConflictDetector()
        self.oscillator = CrystalOscillator()
        self.llm = QwenLocal() if os.getenv("IMMUNE_CRYSTAL_LLM") == "qwen" else StubLLM()

    def inject(
        self,
        content: str,
        domain: str,
        source: str = "manual",
        compliance_tags: list[str] | None = None,
    ) -> BCell:
        domain = domain.strip().lower()
        self.domains.register(domain, content, compliance_tags)
        cell = create_b_cell(content, domain, source, compliance_tags)
        self.store.add(cell)
        self.audit.write(
            AuditRecord(
                event="inject",
                query=content,
                metadata={"cell_id": cell.id, "domain": domain, "tags": compliance_tags or []},
            )
        )
        return cell

    def bootstrap(self, items: list[dict]) -> dict:
        created = []
        for item in items:
            cell = self.inject(
                content=item["content"],
                domain=item["domain"],
                source=item.get("source", "bootstrap"),
                compliance_tags=item.get("compliance_tags", []),
            )
            created.append({"cell_id": cell.id, "domain": cell.domain})
        return {"created": len(created), "items": created}

    def chat(self, query: str, domain: str | None = None) -> ChatResult:
        target_domain = domain.strip().lower() if domain else self.t_cell.route_domain(query)
        detection = self.t_cell.inspect(query, target_domain)
        if not detection.clean:
            self.t_cell.learn(query, target_domain)
            record = self.audit.write(
                AuditRecord(
                    event="blocked",
                    query=query,
                    purity_score=0.0,
                    metadata=detection.model_dump(),
                )
            )
            return ChatResult(
                answer="Blocked by T-Cell pollution detector.",
                purity=0.0,
                lineage=[],
                audit_id=record.id,
                blocked=True,
                reason=detection.reason,
            )

        ranked = self._rank(query, target_domain)
        cells = [cell for cell, _ in ranked]
        scores = [score for _, score in ranked]
        self._handle_conflicts(query, cells)
        for cell in cells:
            reinforce(cell)
            self.store.update(cell)
        answer = self.llm.generate(query, cells)
        lineage = lineage_for(cells)
        purity = purity_score(cells, scores)
        record = self.audit.write(
            AuditRecord(
                event="chat",
                query=query,
                answer=answer,
                purity_score=purity,
                lineage=lineage,
                metadata={"domain": target_domain},
            )
        )
        return ChatResult(answer=answer, purity=purity, lineage=lineage, audit_id=record.id)

    def reset(self, cell_id: str) -> BCell | None:
        cell = self.store.get(cell_id)
        if not cell:
            return None
        reset_to_purifying(cell)
        self.store.update(cell)
        self.audit.write(AuditRecord(event="reset", metadata={"cell_id": cell.id}))
        return cell

    def crystal_state(self) -> list[dict]:
        return [
            {
                "cell": cell.model_dump(),
                "weight": self.oscillator.weight(cell.crystal_state),
                "curve": self.oscillator.curve(cell, points=32, step_seconds=30),
            }
            for cell in self.store.list()
        ]

    def domain_state(self) -> list[dict]:
        return [profile.model_dump() for profile in self.domains.list()]

    def _rank(self, query: str, domain: str) -> list[tuple[BCell, float]]:
        hits = self.store.query(query, domain=domain, limit=6)
        if not hits and domain != "general":
            hits = self.store.query(query, limit=6)
        scored = [(cell, self.oscillator.score(cell, sim)) for cell, sim in hits]
        return sorted(scored, key=lambda item: item[1], reverse=True)[:4]

    def _handle_conflicts(self, query: str, cells: list[BCell]) -> None:
        for cell in cells:
            if self.conflicts.conflict(query, cell.content):
                quarantine_conflict(cell)
                self.store.update(cell)
                self.audit.write(
                    AuditRecord(
                        event="phase_transition",
                        query=query,
                        metadata={"cell_id": cell.id, "reason": "conflict"},
                    )
                )
