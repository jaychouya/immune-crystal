from __future__ import annotations

from core.memory.store import MemoryStore
from core.models import BCell


class Repertoire:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def domains(self) -> list[str]:
        return sorted({cell.domain for cell in self.store.list()})

    def by_domain(self, domain: str) -> list[BCell]:
        return self.store.list(domain)
