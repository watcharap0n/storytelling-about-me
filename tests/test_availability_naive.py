import os
from fastapi.testclient import TestClient

from app.main import create_app

app = create_app()
client = TestClient(app)

headers = {"x-api-key": os.getenv("API_KEY", "test-key")}


def test_availability_date_only_range():
    resp = client.get("/v1/availability", params={"range": "2024-10-19/2024-10-19"}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("free"), list)


def test_availability_naive_datetime_range():
    resp = client.get(
        "/v1/availability",
        params={"range": "2024-10-19T00:00:00/2024-10-19T23:59:59"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("free"), list)

