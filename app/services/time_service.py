"""Time service for returning the current date/time in GMT+7 (Asia/Bangkok)."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Dict, Any

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover - fallback
    ZoneInfo = None  # type: ignore


def _get_bangkok_tz():
    if ZoneInfo is not None:
        try:
            return ZoneInfo("Asia/Bangkok")
        except Exception:
            pass
    # Fallback to fixed UTC+7 offset
    return timezone(timedelta(hours=7))


def get_current_time_gmt7() -> Dict[str, Any]:
    tz = _get_bangkok_tz()
    now = datetime.now(tz=tz)

    # Prefer IANA name when available
    tz_name = "Asia/Bangkok" if ZoneInfo is not None and isinstance(tz, ZoneInfo) else "UTC+7"

    # Compute offset as +HH:MM
    offset_td = now.utcoffset() or timedelta(0)
    total_minutes = int(offset_td.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hh, mm = divmod(abs(total_minutes), 60)
    offset_str = f"{sign}{hh:02d}:{mm:02d}"

    return {
        "time_zone": tz_name,
        "offset": offset_str,
        "datetime_iso": now,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "weekday": now.strftime("%A"),
        "tz_abbr": now.tzname() or "+07",
    }
