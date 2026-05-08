from __future__ import annotations

import json
import os
import re
from pathlib import Path

from core.models import Antibody


class AntibodyRegistry:
    def __init__(self, data_dir: str | None = None) -> None:
        root = data_dir or os.getenv("IMMUNE_CRYSTAL_DATA", "data")
        self.path = Path(root) / "antibodies.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.antibodies: dict[str, Antibody] = {}
        self._load()

    def add(self, pattern: str, domain: str | None = None) -> Antibody:
        for antibody in self.antibodies.values():
            if antibody.pattern == pattern and antibody.domain == domain:
                antibody.hits += 1
                self.save()
                return antibody
        antibody = Antibody(pattern=pattern, domain=domain)
        self.antibodies[antibody.id] = antibody
        self.save()
        return antibody

    def match(self, text: str, domain: str | None = None) -> list[Antibody]:
        hits = []
        for antibody in self.antibodies.values():
            if antibody.domain and domain and antibody.domain != domain:
                continue
            if re.search(antibody.pattern, text, re.IGNORECASE):
                hits.append(antibody)
        return hits

    def list(self) -> list[Antibody]:
        return list(self.antibodies.values())

    def save(self) -> None:
        payload = [item.model_dump() for item in self.antibodies.values()]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if self.path.exists():
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            self.antibodies = {item["id"]: Antibody(**item) for item in payload}
