import os

from fastapi.testclient import TestClient

from app.main import create_app


app = create_app()
client = TestClient(app)
headers = {"x-api-key": os.getenv("API_KEY", "test-key")}


def test_time_now_endpoint_basic():
    resp = client.get("/v1/time/now", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    # Ensure core fields exist
    assert "time_zone" in data
    assert data["offset"].startswith("+") and data["offset"].endswith(":00")
    assert data["offset"] == "+07:00"
    assert isinstance(data.get("year"), int)
    assert 1 <= data.get("month") <= 12
    assert 1 <= data.get("day") <= 31
    # The datetime string should include timezone offset
    assert data["datetime_iso"].endswith("+07:00")


def test_time_now_endpoint_timezone_label():
    resp = client.get("/v1/time/now", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    # Accept either Asia/Bangkok or UTC+7 fallback label
    assert data["time_zone"] in ("Asia/Bangkok", "UTC+7")
