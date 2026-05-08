from __future__ import annotations

from core.memory.store import MemoryStore


class DriftDetector:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def score(self, text: str, domain: str) -> float:
        hits = self.store.query(text, domain=domain, limit=3)
        if not hits:
            return 0.5
        best = max(score for _, score in hits)
        return max(0.0, 1.0 - best)
