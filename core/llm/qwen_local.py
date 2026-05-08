from __future__ import annotations

from core.llm.base import LLMBackend
from core.models import BCell


class QwenLocal(LLMBackend):
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct") -> None:
        self.model_name = model_name
        self._pipeline = None

    def generate(self, query: str, context: list[BCell]) -> str:
        pipe = self._load()
        prompt = self._prompt(query, context)
        output = pipe(prompt, max_new_tokens=256, do_sample=False)
        text = output[0]["generated_text"]
        return text[len(prompt) :].strip() or text

    def _load(self):
        if self._pipeline is None:
            from transformers import pipeline

            self._pipeline = pipeline("text-generation", model=self.model_name, device_map="auto")
        return self._pipeline

    @staticmethod
    def _prompt(query: str, context: list[BCell]) -> str:
        facts = "\n".join(f"[{cell.domain}|{cell.trust_score:.2f}] {cell.content}" for cell in context)
        return (
            "You are immune-crystal, an enterprise AI compliance assistant. "
            "Answer only from trusted context and mention uncertainty when context is insufficient.\n\n"
            f"Trusted context:\n{facts}\n\nQuery: {query}\nAnswer:"
        )
