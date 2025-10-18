"""Contact endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.middleware import verify_api_key
from app.models.schemas import ContactResponse, ContactMessageRequest, ContactMessageResponse
from app.services.contact_service import submit_contact_message
from app.services.data_service import get_contact_channels

router = APIRouter(prefix="/v1/contact", tags=["Contact"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=ContactResponse)
async def read_contact() -> ContactResponse:
    return ContactResponse(channels=get_contact_channels())


@router.post("/message", response_model=ContactMessageResponse)
async def submit_message(payload: ContactMessageRequest, request: Request) -> ContactMessageResponse:
    if payload.honeypot:
        raise HTTPException(status_code=400, detail={"code": "ERR_BAD_REQUEST", "message": "Invalid submission."})

    ticket_id = await submit_contact_message(
        {
            "name": payload.name,
            "email": payload.email,
            "message": payload.message,
            "ip": request.client.host if request.client else None,
        }
    )
    return ContactMessageResponse(ticket_id=ticket_id, submitted_at=datetime.now(tz=timezone.utc))
