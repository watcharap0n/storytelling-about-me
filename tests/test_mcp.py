import os

from fastapi.testclient import TestClient

from app.main import create_app

app = create_app()
client = TestClient(app)

headers = {"x-api-key": os.getenv("API_KEY", "test-key")}


def test_mcp_execute_echo():
    # With no webhook configured, endpoint should echo the request
    payload = {"tool": "ping", "params": {"x": 1}, "context": {"env": "test"}}
    resp = client.post("/v1/mcp/execute", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["forwarded"] is False
    assert "result" in body and "echo" in body["result"]
    assert body["result"]["echo"]["tool"] == "ping"
    assert body["meta"]["webhook_configured"] is False

