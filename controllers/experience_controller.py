"""Controller defining endpoints for experience-related stories."""

from fastapi import APIRouter

from models.experience import ThaicomAIExperience
from services.thaicom_ai_service import get_ai_experience

router = APIRouter()


@router.get("/experience/thaicom/ai", response_model=ThaicomAIExperience)
def read_thaicom_ai_experience() -> ThaicomAIExperience:
    """Expose the AI Engineering story from Thaicom."""

    return get_ai_experience()
