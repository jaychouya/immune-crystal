from __future__ import annotations

from core.service import ImmuneCrystal

service = ImmuneCrystal()


def get_service() -> ImmuneCrystal:
    return service
