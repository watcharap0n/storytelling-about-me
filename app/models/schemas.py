"""Pydantic schemas for API responses."""

from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, HttpUrl


class LinkSet(BaseModel):
    site: Optional[HttpUrl]
    resume: Optional[HttpUrl]
    linkedin: Optional[HttpUrl]
    github: Optional[HttpUrl]


class AboutResponse(BaseModel):
    id: str
    name: str
    title: str
    headline: str
    summary: str
    location: str
    links: LinkSet


class Pillar(BaseModel):
    id: str
    title: str
    bullets: List[str]


class PillarsResponse(BaseModel):
    items: List[Pillar]


class WorkKPI(BaseModel):
    latency_reduction_pct: Optional[int] = None
    ops_cost_reduction_pct: Optional[int] = None
    automations: Optional[int] = None
    teams_onboarded: Optional[int] = None
    p95_latency_lt_2s_pct: Optional[int] = None
    sev1_incidents: Optional[int] = None
    booking_time_reduction_pct: Optional[int] = None
    manual_ops_reduction_pct: Optional[int] = None
    time_to_launch_weeks: Optional[int] = None
    support_tickets_reduction_pct: Optional[int] = None
    completion_lift_pct: Optional[int] = None


class WorkExternal(BaseModel):
    url: Optional[HttpUrl]


class WorkItem(BaseModel):
    slug: str
    title: str
    subtitle: str
    summary: str
    description: Optional[str] = None
    stack: List[str]
    kpi: WorkKPI
    external: Optional[WorkExternal] = None


class WorkListResponse(BaseModel):
    items: List[WorkItem]


class Period(BaseModel):
    start: datetime
    end: Optional[datetime]


class ExperienceItem(BaseModel):
    id: str
    organization: str
    role: str
    period: Period
    location: str
    highlights: List[str]


class ExperienceResponse(BaseModel):
    items: List[ExperienceItem]


class SkillItem(BaseModel):
    name: str
    level: int = Field(ge=1, le=5)
    notes: Optional[str]


class SkillGroup(BaseModel):
    id: str
    title: str
    description: str
    items: List[SkillItem]


class SkillsResponse(BaseModel):
    items: List[SkillGroup]


class Certification(BaseModel):
    id: str
    name: str
    issuer: str
    issued_at: datetime
    notes: Optional[str]
    credential_url: Optional[HttpUrl]


class ContinuingEducationItem(BaseModel):
    id: str
    name: str
    issuer: str
    period: str


class CertificationsResponse(BaseModel):
    items: List[Certification]
    continuing_education: List[ContinuingEducationItem]


class ContactChannels(BaseModel):
    email: Optional[str]
    linkedin: Optional[HttpUrl]
    github: Optional[HttpUrl]


class ContactResponse(BaseModel):
    channels: ContactChannels


class ContactMessageRequest(BaseModel):
    name: str
    email: str
    message: str
    honeypot: Optional[str] = Field(default=None, description="Leave blank")


class ContactMessageResponse(BaseModel):
    ticket_id: str
    submitted_at: datetime


class AvailabilityWindow(BaseModel):
    start: datetime
    end: datetime


class AvailabilityResponse(BaseModel):
    generated_at: datetime
    time_zone: str
    free: List[AvailabilityWindow]


class AvailabilityHoldRequest(BaseModel):
    start: datetime
    end: datetime
    requester: Optional[str]


class AvailabilityHoldResponse(BaseModel):
    hold_id: str
    expires_at: datetime


class ChatRequest(BaseModel):
    question: str
    audience: Optional[str] = Field(default="general", pattern="^(recruiter|engineer|general)$")


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    suggestions: List[str]
    events: List[dict]


class ErrorResponse(BaseModel):
    error: dict


class MetaResponse(BaseModel):
    version: str
    environment: str


class IndexResource(BaseModel):
    name: str
    method: str
    path: str
    description: str


class IndexResponse(BaseModel):
    resources: List[IndexResource]


# New MCP schemas
class MCPRequest(BaseModel):
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    context: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    forwarded: bool
    result: Dict[str, Any] = Field(default_factory=dict)
    meta: Optional[Dict[str, Any]] = None


# New: long-form work content
class WorkContentResponse(BaseModel):
    slug: str
    format: str = Field(description="Content format, e.g., markdown or html")
    content: str


# New: current time (GMT+7) response schema
class CurrentTimeResponse(BaseModel):
    time_zone: str = Field(description="IANA time zone, e.g., Asia/Bangkok")
    offset: str = Field(description="UTC offset in +HH:MM format")
    datetime_iso: datetime = Field(description="Current time in GMT+7 (timezone-aware)")
    date: str = Field(description="YYYY-MM-DD in GMT+7")
    time: str = Field(description="HH:MM:SS in GMT+7")
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    weekday: str = Field(description="Weekday name in English, e.g., Monday")
    tz_abbr: str = Field(description="Time zone abbreviation, e.g., +07 or ICT")
