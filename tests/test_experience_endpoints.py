"""Unit tests for career storytelling endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mango_experience():
    """Ensure Mango endpoint returns the correct company name."""
    response = client.get("/experience/mango")
    assert response.status_code == 200
    payload = response.json()
    assert payload["company"] == "Mango Consultant"


def test_thaicom_ai_experience():
    """Ensure Thaicom AI endpoint returns the correct role."""
    response = client.get("/experience/thaicom/ai")
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "AI Engineer"


def test_thaicom_genai_experience():
    """Ensure GenAI endpoint returns expected highlight."""
    response = client.get("/experience/thaicom/genai")
    assert response.status_code == 200
    payload = response.json()
    assert "AI4ALL" in payload["highlights"][0]
