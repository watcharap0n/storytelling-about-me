"""Service functions backed by seed data."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from dateutil import parser

from app.services.data_loader import SEED_DATA


def get_about() -> Dict[str, Any]:
    return SEED_DATA["about"]


def get_pillars() -> List[Dict[str, Any]]:
    return SEED_DATA["pillars"]


def get_work_items(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    items = SEED_DATA["work"]
    if limit:
        return items[:limit]
    return items


def get_work_item(slug: str) -> Optional[Dict[str, Any]]:
    return next((item for item in SEED_DATA["work"] if item["slug"] == slug), None)


def get_experience() -> List[Dict[str, Any]]:
    experience = SEED_DATA["experience"]
    for item in experience:
        item["period"]["start"] = parser.isoparse(item["period"]["start"]).isoformat()
        if item["period"].get("end"):
            item["period"]["end"] = parser.isoparse(item["period"]["end"]).isoformat()
        else:
            item["period"]["end"] = None
    return experience


def get_skills() -> List[Dict[str, Any]]:
    return SEED_DATA["skills"]


def get_certifications() -> Dict[str, Any]:
    certs = [
        {
            **cert,
            "issued_at": parser.isoparse(cert["issued_at"]).isoformat(),
        }
        for cert in SEED_DATA["certifications"]
    ]
    return {
        "items": certs,
        "continuing_education": SEED_DATA.get("continuing_education", []),
    }


def get_contact_channels() -> Dict[str, Any]:
    return SEED_DATA["contact"]["channels"]


def get_availability() -> Dict[str, Any]:
    data = SEED_DATA["availability"].copy()
    data["generated_at"] = parser.isoparse(data["generated_at"]).isoformat()
    data["free"] = [
        {"start": parser.isoparse(slot["start"]).isoformat(), "end": parser.isoparse(slot["end"]).isoformat()}
        for slot in data["free"]
    ]
    return data


def get_faq_entries() -> List[Dict[str, Any]]:
    return SEED_DATA.get("faq", [])
