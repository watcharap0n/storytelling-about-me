"""About endpoint."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import AboutResponse
from app.services.data_service import get_about

router = APIRouter(prefix="/v1/about", tags=["About"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=AboutResponse)
async def read_about() -> AboutResponse:
    return AboutResponse(**get_about())
