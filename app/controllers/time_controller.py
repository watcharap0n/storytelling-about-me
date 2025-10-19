"""Time endpoints (GMT+7)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import CurrentTimeResponse
from app.services.time_service import get_current_time_gmt7

router = APIRouter(prefix="/v1/time", tags=["Time"], dependencies=[Depends(verify_api_key)])


@router.get("/now", response_model=CurrentTimeResponse)
async def current_time_now() -> CurrentTimeResponse:
    data = get_current_time_gmt7()
    return CurrentTimeResponse(**data)

