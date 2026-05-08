from __future__ import annotations

import re


APPROVE = {"approve", "批准", "通过", "grant", "accept"}
REJECT = {"reject", "拒绝", "deny", "驳回", "decline"}


class ConflictDetector:
    def score(self, left: str, right: str) -> float:
        l = left.lower()
        r = right.lower()
        if self._has(l, APPROVE) and self._has(r, REJECT):
            return 0.92
        if self._has(l, REJECT) and self._has(r, APPROVE):
            return 0.92
        if self._same_entity(left, right) and self._opposite_polarity(l, r):
            return 0.86
        return 0.0

    def conflict(self, left: str, right: str, threshold: float = 0.85) -> bool:
        return self.score(left, right) >= threshold

    @staticmethod
    def _has(text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)

    @staticmethod
    def _opposite_polarity(left: str, right: str) -> bool:
        neg = {"not", "不得", "不能", "禁止", "no"}
        return any(n in left for n in neg) != any(n in right for n in neg)

    @staticmethod
    def _same_entity(left: str, right: str) -> bool:
        left_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", left))
        right_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", right))
        return bool(left_tokens & right_tokens)
