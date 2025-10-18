"""Utility to load seed data for the API."""

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "seed.json"


def load_seed_data() -> dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


SEED_DATA = load_seed_data()
