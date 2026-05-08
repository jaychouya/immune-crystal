from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_service
from api.schemas import BootstrapRequest, InjectRequest
from core.service import ImmuneCrystal

router = APIRouter()


@router.post("/inject")
def inject(payload: InjectRequest, service: ImmuneCrystal = Depends(get_service)):
    return service.inject(
        content=payload.content,
        domain=payload.domain,
        source=payload.source,
        compliance_tags=payload.compliance_tags,
    )


@router.post("/bootstrap")
def bootstrap(payload: BootstrapRequest, service: ImmuneCrystal = Depends(get_service)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="items cannot be empty")
    return service.bootstrap([item.model_dump() for item in payload.items])
