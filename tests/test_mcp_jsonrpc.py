import os
from fastapi.testclient import TestClient

from app.main import create_app

app = create_app()
client = TestClient(app)

headers = {"x-api-key": os.getenv("API_KEY", "test-key")}


def test_mcp_jsonrpc_initialize_local():
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "n8n-mcp", "version": "1.0"},
        },
    }
    resp = client.post("/v1/mcp/execute", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("jsonrpc") == "2.0"
    assert body.get("id") == 0
    assert "result" in body
    assert body["result"]["protocolVersion"] == "2025-03-26"
    assert "serverInfo" in body["result"]


def test_mcp_jsonrpc_tools_list_local():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    }
    resp = client.post("/v1/mcp/execute", json=payload, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("jsonrpc") == "2.0"
    assert body.get("id") == 1
    assert "result" in body and "tools" in body["result"]
    tools = body["result"]["tools"]
    assert isinstance(tools, list)
    # At least one tool should exist per manifest
    assert any(isinstance(t.get("name"), str) for t in tools)

