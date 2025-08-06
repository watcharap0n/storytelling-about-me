"""Pydantic models describing professional experiences.

This module defines schemas used by the API to serialise
career milestones. Only the "GenAI & AI4ALL" experience is
currently modelled.
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel


class GenAIProject(BaseModel):
    """Represents a single project within the GenAI & AI4ALL initiative."""

    name: str
    description: str


class ThaicomGenAIExperience(BaseModel):
    """Schema capturing the GenAI & AI4ALL experience at Thaicom.

    Attributes
    ----------
    role: str
        Primary position held during the initiative.
    projects: List[GenAIProject]
        Key projects delivered as part of the programme.
    """

    role: str
    projects: List[GenAIProject]


