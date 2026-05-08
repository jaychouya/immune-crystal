from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    domain: Optional[str] = None


class InjectRequest(BaseModel):
    content: str
    domain: str
    source: str = "manual"
    compliance_tags: list[str] = []


class BootstrapItem(BaseModel):
    content: str
    domain: str
    source: str = "bootstrap"
    compliance_tags: list[str] = []


class BootstrapRequest(BaseModel):
    items: list[BootstrapItem]


class PoisonRequest(BaseModel):
    text: str
    domain: Optional[str] = None
