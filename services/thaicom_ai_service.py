"""Service layer providing the AI Engineering experience at Thaicom."""

from models.experience import ThaicomAIExperience


def get_ai_experience() -> ThaicomAIExperience:
    """Return the AI Engineering experience schema."""

    return ThaicomAIExperience()
