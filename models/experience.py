from pydantic import BaseModel
from typing import List


class Experience(BaseModel):
    """Represents a professional experience with a role and notable achievements."""

    role: str
    achievements: List[str]


class ThaicomAIExperience(Experience):
    """Schema capturing the AI Engineering role and achievements at Thaicom."""

    role: str = "AI Engineer"
    achievements: List[str] = [
        "Implemented robust machine learning deployment pipelines using SageMaker and MLflow.",
        "Engineered real-time inference systems via Lambda and API Gateway, significantly reducing response times.",
        "Led technical efforts in geospatial AI projects such as forestry analysis and carbon assessment.",
    ]
