"""API routes exposing professional experiences."""

from fastapi import APIRouter

from models.experience import ThaicomGenAIExperience
from services.thaicom_genai_service import get_genai_experience

router = APIRouter(prefix="/experience", tags=["experience"])


@router.get("/thaicom/genai", response_model=ThaicomGenAIExperience)
async def get_thaicom_genai_experience() -> ThaicomGenAIExperience:
    """Retrieve the GenAI & AI4ALL initiative details."""

    return get_genai_experience()


