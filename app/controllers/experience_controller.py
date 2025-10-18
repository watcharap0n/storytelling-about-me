"""Experience endpoints."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import ExperienceResponse, ExperienceItem, Period
from app.services.data_service import get_experience

router = APIRouter(prefix="/v1/experience", tags=["Experience"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=ExperienceResponse)
async def list_experience() -> ExperienceResponse:
    items = []
    for exp in get_experience():
        period = Period(start=exp["period"]["start"], end=exp["period"]["end"])
        items.append(
            ExperienceItem(
                id=exp["id"],
                organization=exp["organization"],
                role=exp["role"],
                period=period,
                location=exp["location"],
                highlights=exp["highlights"],
            )
        )
    return ExperienceResponse(items=items)
