"""Service for processing contact messages."""

from datetime import datetime, timezone
from typing import Dict

import httpx

from app.core.config import get_settings


async def submit_contact_message(payload: Dict) -> str:
    settings = get_settings()
    ticket_id = payload.get("ticket_id")
    if not ticket_id:
        ticket_id = f"ticket_{int(datetime.now(tz=timezone.utc).timestamp())}"

    webhook = settings.n8n_contact_webhook
    if webhook:
        async with httpx.AsyncClient(timeout=settings.n8n_contact_timeout_seconds) as client:
            await client.post(str(webhook), json={**payload, "ticket_id": ticket_id})

    return ticket_id
