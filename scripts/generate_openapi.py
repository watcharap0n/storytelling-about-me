"""Script to export OpenAPI schema to openapi.yaml."""

import json
from pathlib import Path

import yaml  # type: ignore
from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    client = TestClient(app)
    response = client.get("/openapi.json")
    response.raise_for_status()
    schema = response.json()
    target = Path("openapi.yaml")
    target.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
    print(f"OpenAPI schema written to {target}")


if __name__ == "__main__":
    main()
