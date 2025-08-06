"""Controllers exposing career storytelling endpoints."""

from fastapi import APIRouter

from app.models.experience import Experience
from app.services.experience_service import (
    get_mango_experience,
    get_thaicom_ai_experience,
    get_thaicom_genai_experience,
)

router = APIRouter(prefix="/experience", tags=["experience"])


@router.get("/mango", response_model=Experience)
def read_mango_experience() -> Experience:
    """Endpoint returning Mango Consultant experience."""
    return get_mango_experience()


@router.get("/thaicom/ai", response_model=Experience)
def read_thaicom_ai_experience() -> Experience:
    """Endpoint returning Thaicom AI engineering experience."""
    return get_thaicom_ai_experience()


@router.get("/thaicom/genai", response_model=Experience)
def read_thaicom_genai_experience() -> Experience:
    """Endpoint returning GenAI & AI4ALL initiative experience."""
    return get_thaicom_genai_experience()
