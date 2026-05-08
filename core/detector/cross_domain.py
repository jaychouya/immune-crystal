from __future__ import annotations

from core.domain import DomainRegistry


class CrossDomainDetector:
    def __init__(self) -> None:
        self.registry = DomainRegistry()

    def score(self, text: str, target_domain: str) -> float:
        detected = self.registry.route(text)
        if detected == "general" or detected == target_domain:
            return 0.0
        return 0.85
