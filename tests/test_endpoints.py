import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

os.environ.setdefault("API_KEY", "test-key")

app = create_app()
client = TestClient(app)

headers = {"x-api-key": "test-key"}


def test_about():
    response = client.get("/v1/about", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == "about_01"


def test_work_detail():
    response = client.get("/v1/work/carbon-watch", headers=headers)
    assert response.status_code == 200
    assert response.json()["slug"] == "carbon-watch"


def test_contact_message_validation():
    response = client.post(
        "/v1/contact/message",
        headers=headers,
        json={"name": "Alex", "email": "alex@example.com", "message": "Hi Kane!"},
    )
    assert response.status_code == 200
    assert "ticket_id" in response.json()


def test_availability_range_filter():
    response = client.get(
        "/v1/availability",
        params={"range": "2024-10-19T00:00:00+07:00/2024-10-19T23:59:59+07:00"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["free"]) >= 1
