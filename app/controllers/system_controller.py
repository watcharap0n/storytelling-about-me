"""System endpoints such as health checks and resource index."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.core.middleware import verify_api_key
from app.models.schemas import IndexResponse, IndexResource, MetaResponse

router = APIRouter()


@router.get("/healthz", tags=["System"])
async def healthz() -> dict:
    return {"status": "ok", "timestamp": datetime.now(tz=timezone.utc).isoformat()}


@router.get("/v1/meta", response_model=MetaResponse, tags=["System"], dependencies=[Depends(verify_api_key)])
async def meta() -> MetaResponse:
    settings = get_settings()
    return MetaResponse(version=settings.app_version, environment=settings.environment)


@router.get("/v1", response_model=IndexResponse, tags=["System"], dependencies=[Depends(verify_api_key)])
async def index() -> IndexResponse:
    resources = [
        IndexResource(name="about", method="GET", path="/v1/about", description="Profile and headline"),
        IndexResource(name="pillars", method="GET", path="/v1/pillars", description="Capability pillars"),
        IndexResource(name="work", method="GET", path="/v1/work", description="Case studies"),
        IndexResource(name="experience", method="GET", path="/v1/experience", description="Career timeline"),
        IndexResource(name="skills", method="GET", path="/v1/skills", description="Skill groups"),
        IndexResource(name="certifications", method="GET", path="/v1/certifications", description="Credentials"),
        IndexResource(name="contact", method="GET", path="/v1/contact", description="Contact channels"),
        IndexResource(name="contact_message", method="POST", path="/v1/contact/message", description="Submit contact message"),
        IndexResource(name="availability", method="GET", path="/v1/availability", description="Free/busy windows"),
        IndexResource(name="availability_hold", method="POST", path="/v1/availability/hold", description="Create temporary hold"),
        IndexResource(name="chat", method="POST", path="/v1/chat/ask", description="Ask portfolio assistant"),
        IndexResource(name="time_now", method="GET", path="/v1/time/now", description="Current date/time in GMT+7 (Asia/Bangkok)"),
        IndexResource(name="mcp_execute", method="POST", path="/v1/mcp/execute", description="Forward MCP request to n8n or echo"),
    ]
    return IndexResponse(resources=resources)
