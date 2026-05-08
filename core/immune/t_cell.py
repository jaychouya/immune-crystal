from __future__ import annotations

import re

from core.domain import DomainRegistry
from core.immune.antibody import AntibodyRegistry
from core.models import DetectionResult


INJECTION_PATTERNS = [
    r"ignore previous",
    r"system prompt",
    r"developer message",
    r"越权",
    r"忽略.*规则",
    r"泄露",
]


class TCell:
    def __init__(
        self,
        antibodies: AntibodyRegistry | None = None,
        registry: DomainRegistry | None = None,
    ) -> None:
        self.antibodies = antibodies or AntibodyRegistry()
        self.registry = registry or DomainRegistry()

    def route_domain(self, text: str) -> str:
        return self.registry.route(text)

    def inspect(self, text: str, target_domain: str | None = None) -> DetectionResult:
        domain = target_domain or self.route_domain(text)
        matched = self.antibodies.match(text, domain)
        score = 0.0
        reasons = []
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.6
                reasons.append(pattern)
        if matched:
            score += min(0.45, 0.15 * len(matched))
            reasons.extend([item.pattern for item in matched])
        text_domain = self.route_domain(text)
        if target_domain and text_domain not in {target_domain, "general"}:
            score += 0.6
            reasons.append(f"cross-domain:{text_domain}->{target_domain}")
        foreign_hits = self.registry.foreign_sensitive_hits(text, target_domain)
        if foreign_hits:
            score += min(0.8, 0.35 * len(foreign_hits))
            reasons.append("foreign-sensitive:" + ",".join(foreign_hits))
        score = min(1.0, score)
        return DetectionResult(
            clean=score < 0.55,
            pollution_prob=score,
            reason=", ".join(reasons) or "clean",
            matched_antibodies=[item.id for item in matched],
            target_domain=domain,
        )

    def learn(self, text: str, domain: str | None = None) -> None:
        words = re.findall(r"[\w\u4e00-\u9fff]{3,}", text)
        if words:
            pattern = re.escape(" ".join(words[:4]))
            self.antibodies.add(pattern, domain)
