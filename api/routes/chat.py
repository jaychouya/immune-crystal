from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import get_service
from api.schemas import ChatRequest, PoisonRequest
from core.service import ImmuneCrystal

router = APIRouter()


@router.post("/chat")
def chat(payload: ChatRequest, service: ImmuneCrystal = Depends(get_service)):
    return service.chat(payload.query, payload.domain)


@router.post("/poison/test")
def poison(payload: PoisonRequest, service: ImmuneCrystal = Depends(get_service)):
    detection = service.t_cell.inspect(payload.text, payload.domain)
    if not detection.clean:
        service.t_cell.learn(payload.text, payload.domain)
    return detection
