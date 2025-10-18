"""MCP forwarding endpoints for n8n integrations."""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Any, Dict
import json as _json

from app.core.middleware import verify_api_key
from app.core.config import get_settings
from app.models.schemas import MCPRequest, MCPResponse
from app.services.mcp_service import forward_mcp_request, forward_jsonrpc_to_n8n

router = APIRouter(prefix="/v1/mcp", tags=["MCP"], dependencies=[Depends(verify_api_key)])


@router.post("/execute")
async def execute_mcp(payload: Dict[str, Any], request: Request):
    print("Received MCP execute request:", payload)
    correlation_id = getattr(request.state, "correlation_id", None)
    settings = get_settings()

    # Detect JSON-RPC 2.0 envelope
    is_jsonrpc = isinstance(payload, dict) and "jsonrpc" in payload and "method" in payload

    if is_jsonrpc:
        ok, forwarded, upstream_json, error = await forward_jsonrpc_to_n8n({**payload, "correlation_id": correlation_id})
        if not ok:
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "error": {
                    "code": -32000,
                    "message": error or "Upstream error.",
                    "data": {"correlation_id": correlation_id},
                },
            }
        # Ensure metadata is included when we are in local fallback
        if not forwarded and isinstance(upstream_json, dict) and upstream_json.get("result") is not None:
            result = upstream_json.get("result")
            if isinstance(result, dict):
                result.setdefault("meta", {})
                result["meta"].update({
                    "webhook_configured": bool(settings.n8n_mcp_webhook),
                    "correlation_id": correlation_id,
                })
        # If forwarded, normalize to MCP content when upstream isn't MCP-shaped
        if forwarded and isinstance(upstream_json, dict):
            if "jsonrpc" not in upstream_json:
                # Wrap plain JSON into JSON-RPC content array
                text_content = _json.dumps(upstream_json, ensure_ascii=False) if not isinstance(upstream_json, str) else upstream_json
                return {
                    "jsonrpc": "2.0",
                    "id": payload.get("id"),
                    "result": {
                        "content": [{"type": "text", "text": text_content}],
                        "isError": False,
                    },
                }
            # Has jsonrpc but missing content array in result
            if upstream_json.get("error") is None:
                res = upstream_json.get("result")
                if not isinstance(res, dict) or "content" not in res:
                    text_content = _json.dumps(res, ensure_ascii=False)
                    upstream_json["result"] = {
                        "content": [{"type": "text", "text": text_content}],
                        "isError": False,
                    }
            return upstream_json
        return upstream_json

    # Fallback to the original simple schema (tool/params/context)
    try:
        simple = MCPRequest(**payload)
    except Exception:
        raise HTTPException(status_code=422, detail={"code": "ERR_BAD_REQUEST", "message": "Invalid MCP payload."})

    ok, forwarded, result, error = await forward_mcp_request(
        {
            "tool": simple.tool,
            "params": simple.params,
            "context": simple.context or {},
            "correlation_id": correlation_id,
        }
    )

    if not ok:
        raise HTTPException(status_code=502, detail={"code": "ERR_UPSTREAM", "message": error or "Upstream error."})

    meta = {
        "webhook_configured": bool(settings.n8n_mcp_webhook),
        "correlation_id": correlation_id,
    }
    return MCPResponse(forwarded=forwarded, result=result or {}, meta=meta)
