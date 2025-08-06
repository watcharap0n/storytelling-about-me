"""Pydantic data models for career experience endpoints."""

from typing import List
from pydantic import BaseModel


class Experience(BaseModel):
    """Represents a single career experience entry."""

    company: str
    period: str
    role: str
    highlights: List[str]
