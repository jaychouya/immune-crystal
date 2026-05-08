from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_service
from core.service import ImmuneCrystal

router = APIRouter()


@router.get("/crystal/state")
def state(service: ImmuneCrystal = Depends(get_service)):
    return service.crystal_state()


@router.get("/domains")
def domains(service: ImmuneCrystal = Depends(get_service)):
    return service.domain_state()


@router.post("/crystal/reset/{cell_id}")
def reset(cell_id: str, service: ImmuneCrystal = Depends(get_service)):
    cell = service.reset(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="cell not found")
    return cell
