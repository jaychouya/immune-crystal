from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

from core.models import BCell


class MemoryStore:
    def __init__(self, data_dir: str | None = None) -> None:
        root = data_dir or os.getenv("IMMUNE_CRYSTAL_DATA", "data")
        self.data_dir = Path(root)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "cells.json"
        self.cells: dict[str, BCell] = {}
        self._load()

    def add(self, cell: BCell) -> BCell:
        if not cell.embedding:
            cell.embedding = self.embed(cell.content)
        self.cells[cell.id] = cell
        self.save()
        return cell

    def list(self, domain: str | None = None) -> list[BCell]:
        values = list(self.cells.values())
        if domain:
            values = [c for c in values if c.domain == domain]
        return sorted(values, key=lambda c: c.updated_at, reverse=True)

    def get(self, cell_id: str) -> BCell | None:
        return self.cells.get(cell_id)

    def update(self, cell: BCell) -> None:
        self.cells[cell.id] = cell
        self.save()

    def query(self, text: str, domain: str | None = None, limit: int = 5) -> list[tuple[BCell, float]]:
        query_embedding = self.embed(text)
        scored = []
        for cell in self.list(domain):
            scored.append((cell, self.cosine(query_embedding, cell.embedding)))
        return sorted(scored, key=lambda item: item[1], reverse=True)[:limit]

    def save(self) -> None:
        payload = [cell.model_dump() for cell in self.cells.values()]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if not self.path.exists():
            return
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        self.cells = {item["id"]: BCell(**item) for item in payload}

    @staticmethod
    def embed(text: str, dim: int = 384) -> list[float]:
        vec = [0.0] * dim
        tokens = text.lower().split()
        if len(tokens) <= 1:
            compact = "".join(text.lower().split())
            tokens = [compact[i : i + 2] for i in range(max(1, len(compact) - 1))]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "big") % dim
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        if not a or not b:
            return 0.0
        size = min(len(a), len(b))
        return sum(a[i] * b[i] for i in range(size))
