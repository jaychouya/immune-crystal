from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import BCell


class LLMBackend(ABC):
    @abstractmethod
    def generate(self, query: str, context: list[BCell]) -> str:
        raise NotImplementedError


class StubLLM(LLMBackend):
    def generate(self, query: str, context: list[BCell]) -> str:
        if not context:
            return "No trusted enterprise memory matched this query."
        facts = "\n".join(f"- [{cell.domain}] {cell.content}" for cell in context[:4])
        return f"Answer grounded in immune-crystal memory:\n{facts}\n\nDecision request: {query}"
