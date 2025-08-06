from pydantic import BaseModel
from typing import List


class Experience(BaseModel):
    """Represents details of a professional role."""

    role: str  # Job title or position held
    responsibilities: List[str]  # Major tasks or accomplishments
    start_date: str  # When the role began
    end_date: str  # When the role ended
