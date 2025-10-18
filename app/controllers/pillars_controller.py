"""Pillars endpoints."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import PillarsResponse
from app.services.data_service import get_pillars

router = APIRouter(prefix="/v1/pillars", tags=["Pillars"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=PillarsResponse)
async def list_pillars() -> PillarsResponse:
    return PillarsResponse(items=[pillar for pillar in get_pillars()])
