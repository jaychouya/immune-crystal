from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from pydantic import BaseModel, Field


class DomainProfile(BaseModel):
    name: str
    description: str = ""
    keywords: list[str] = Field(default_factory=list)
    sensitive_terms: list[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class DomainRegistry:
    def __init__(self, data_dir: str | None = None) -> None:
        root = data_dir or os.getenv("IMMUNE_CRYSTAL_DATA", "data")
        self.path = Path(root) / "domains.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.profiles: dict[str, DomainProfile] = {}
        self._load()

    def register(
        self,
        name: str,
        content: str = "",
        tags: list[str] | None = None,
        description: str = "",
    ) -> DomainProfile:
        profile = self.profiles.get(name) or DomainProfile(name=name, description=description)
        tokens = self.extract_terms(content) + [tag.lower() for tag in tags or []]
        profile.keywords = self._merge(profile.keywords, tokens[:80])
        profile.sensitive_terms = self._merge(profile.sensitive_terms, tokens[:30])
        if description:
            profile.description = description
        profile.updated_at = time.time()
        self.profiles[name] = profile
        self.save()
        return profile

    def route(self, text: str) -> str:
        if not self.profiles:
            return "general"
        lowered = text.lower()
        scores = {}
        for name, profile in self.profiles.items():
            terms = set(profile.keywords + profile.sensitive_terms)
            scores[name] = sum(1 for term in terms if term and term in lowered)
        best, score = max(scores.items(), key=lambda item: item[1])
        return best if score > 0 else "general"

    def foreign_sensitive_hits(self, text: str, target_domain: str | None) -> list[str]:
        lowered = text.lower()
        hits = []
        for name, profile in self.profiles.items():
            if name == target_domain:
                continue
            if any(term and term in lowered for term in profile.sensitive_terms):
                hits.append(name)
        return hits

    def list(self) -> list[DomainProfile]:
        return sorted(self.profiles.values(), key=lambda item: item.name)

    def save(self) -> None:
        payload = [profile.model_dump() for profile in self.profiles.values()]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if not self.path.exists():
            return
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        self.profiles = {item["name"]: DomainProfile(**item) for item in payload}

    @staticmethod
    def extract_terms(text: str) -> list[str]:
        raw = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}|[\u4e00-\u9fff]{2,}", text.lower())
        terms = []
        for item in raw:
            if re.fullmatch(r"[\u4e00-\u9fff]+", item):
                terms.append(item)
                for size in (2, 3, 4):
                    terms.extend(item[i : i + size] for i in range(0, max(0, len(item) - size + 1)))
            elif len(item) <= 8:
                terms.append(item)
            else:
                terms.extend(item[i : i + 4] for i in range(0, len(item) - 3, 2))
        return terms

    @staticmethod
    def _merge(left: list[str], right: list[str]) -> list[str]:
        seen = set()
        result = []
        for item in left + right:
            if item and item not in seen:
                seen.add(item)
                result.append(item)
        return result[:128]
