"""Availability utilities."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from dateutil import parser, tz

from app.services.data_service import get_availability


def _ensure_aware(dt: datetime, zone_name: str) -> datetime:
    """Attach timezone to naive datetimes using the provided zone; return as aware."""
    if dt.tzinfo is None:
        zone = tz.gettz(zone_name) or timezone.utc
        return dt.replace(tzinfo=zone)
    return dt


def _parse_range_component(raw: str, zone_name: str, is_end: bool = False) -> datetime:
    """Parse an ISO-like datetime or date string and ensure tz-aware. For date-only, expand to start/end of day."""
    raw = raw.strip()
    # Date-only e.g. 2024-10-19
    if "T" not in raw and len(raw) == 10:
        y, m, d = [int(x) for x in raw.split("-")]
        if is_end:
            dt = datetime(y, m, d, 23, 59, 59, 999999)
        else:
            dt = datetime(y, m, d, 0, 0, 0, 0)
        return _ensure_aware(dt, zone_name)
    # Full datetime
    dt = parser.isoparse(raw)
    return _ensure_aware(dt, zone_name)


def filter_availability(range_param: Optional[str]) -> dict:
    data = get_availability()
    free_slots = data["free"]
    if range_param:
        try:
            start_str, end_str = range_param.split("/")
            zone_name = data.get("time_zone", "UTC")
            range_start = _parse_range_component(start_str, zone_name, is_end=False)
            range_end = _parse_range_component(end_str, zone_name, is_end=True)
            free_slots = [
                slot
                for slot in free_slots
                if parser.isoparse(slot["end"]) > range_start and parser.isoparse(slot["start"]) < range_end
            ]
        except ValueError:
            # Bad range input; ignore filter
            pass
    return {**data, "free": free_slots}


def create_hold(start: datetime, end: datetime, requester: Optional[str] = None) -> dict:
    hold_id = f"hold_{int(datetime.now(tz=timezone.utc).timestamp())}"
    expires_at = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
    return {
        "hold_id": hold_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "requester": requester,
        "expires_at": expires_at.isoformat(),
    }
