"""Content service for long-form project writeups (no database).

Reads Markdown files from data/content/work/{slug}.md and returns them.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict


def get_work_content(slug: str) -> Dict[str, str]:
    if not slug or "/" in slug or ".." in slug:
        raise FileNotFoundError("Invalid slug")
    # Resolve repository root and content path
    root = Path(__file__).resolve().parents[2]
    md_path = root / "data" / "content" / "work" / f"{slug}.md"
    if not md_path.exists():
        raise FileNotFoundError(f"Content not found for slug: {slug}")
    content = md_path.read_text(encoding="utf-8")
    return {"slug": slug, "format": "markdown", "content": content}

