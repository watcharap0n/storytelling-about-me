"""Availability endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.middleware import verify_api_key
from app.models.schemas import AvailabilityResponse, AvailabilityHoldRequest, AvailabilityHoldResponse
from app.services.availability_service import create_hold, filter_availability

router = APIRouter(prefix="/v1/availability", tags=["Availability"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=AvailabilityResponse)
async def get_availability(range: str | None = Query(default=None, description="ISO interval e.g. 2024-10-01/2024-10-31")) -> AvailabilityResponse:
    data = filter_availability(range)
    return AvailabilityResponse(**data)


@router.post("/hold", response_model=AvailabilityHoldResponse)
async def create_availability_hold(payload: AvailabilityHoldRequest) -> AvailabilityHoldResponse:
    if payload.end <= payload.start:
        raise HTTPException(status_code=400, detail={"code": "ERR_BAD_REQUEST", "message": "End must be after start."})
    hold = create_hold(payload.start, payload.end, payload.requester)
    return AvailabilityHoldResponse(hold_id=hold["hold_id"], expires_at=datetime.fromisoformat(hold["expires_at"]))
