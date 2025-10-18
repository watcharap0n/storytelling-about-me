"""Skills endpoints."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import SkillsResponse, SkillGroup
from app.services.data_service import get_skills

router = APIRouter(prefix="/v1/skills", tags=["Skills"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=SkillsResponse)
async def list_skills() -> SkillsResponse:
    items = [SkillGroup(**group) for group in get_skills()]
    return SkillsResponse(items=items)
