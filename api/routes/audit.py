from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_service
from core.service import ImmuneCrystal

router = APIRouter()


@router.get("/audit")
def list_audit(service: ImmuneCrystal = Depends(get_service)):
    return service.audit.list()


@router.get("/audit/{audit_id}")
def get_audit(audit_id: str, service: ImmuneCrystal = Depends(get_service)):
    record = service.audit.get(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="audit record not found")
    return record
