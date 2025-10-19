"""Service for forwarding MCP-style requests to n8n or providing a local fallback."""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, List

import httpx
from pathlib import Path
import json

from app.core.config import get_settings
from app.services.data_service import (
    get_about,
    get_pillars,
    get_work_items,
    get_work_item,
    get_experience,
    get_skills,
    get_certifications,
)
from app.services.availability_service import filter_availability
from app.services.chat_service import answer_question
from app.services.contact_service import submit_contact_message
from app.services.content_service import get_work_content  # added
from app.services.time_service import get_current_time_gmt7  # new


def _load_mcp_tools() -> List[Dict[str, Any]]:
    # Load tool definitions from mcp.tools.json at repo root
    try:
        root = Path(__file__).resolve().parents[2]
        manifest = root / "mcp.tools.json"
        tools = json.loads(manifest.read_text(encoding="utf-8"))
        # Normalize keys if needed (ensure inputSchema key)
        normalized: List[Dict[str, Any]] = []
        for t in tools:
            normalized.append(
                {
                    "name": t.get("name"),
                    "description": t.get("description"),
                    "inputSchema": t.get("input_schema", {}),
                }
            )
        return normalized
    except Exception:
        return []


async def forward_mcp_request(payload: Dict[str, Any]) -> Tuple[bool, bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Forward the MCP request to n8n if configured, otherwise echo back the payload locally.

    Returns (ok, forwarded, result, error_message)
    """
    settings = get_settings()
    webhook = settings.n8n_mcp_webhook

    if not webhook:
        # Local echo fallback in dev/test
        return True, False, {"echo": payload}, None

    try:
        async with httpx.AsyncClient(timeout=settings.n8n_mcp_timeout_seconds) as client:
            resp = await client.post(str(webhook), json=payload)
            resp.raise_for_status()
            # Try parse JSON; if not JSON, wrap text
            try:
                result = resp.json()
            except ValueError:
                result = {"text": resp.text}
            return True, True, result, None
    except httpx.HTTPError as e:
        return False, True, None, str(e)


async def _execute_local_tool(name: str, arguments: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Execute known tools locally using internal services.
    Returns (ok, result, error)
    """
    try:
        if name == "get_about":
            return True, {"about": get_about()}, None
        if name == "list_pillars":
            return True, {"items": get_pillars()}, None
        if name == "list_work":
            limit = arguments.get("limit")
            return True, {"items": get_work_items(limit=limit)}, None
        if name == "get_work":
            slug = arguments.get("slug")
            if not slug:
                return False, None, {"code": "ERR_BAD_REQUEST", "message": "Missing 'slug'"}
            item = get_work_item(slug)
            if not item:
                return False, None, {"code": "ERR_NOT_FOUND", "message": "Work item not found"}
            return True, {"item": item}, None
        if name == "get_work_content":
            slug = arguments.get("slug")
            if not slug:
                return False, None, {"code": "ERR_BAD_REQUEST", "message": "Missing 'slug'"}
            try:
                content = get_work_content(slug)
            except FileNotFoundError:
                return False, None, {"code": "ERR_NOT_FOUND", "message": "Content not found"}
            return True, {"content": content}, None
        if name == "list_experience":
            return True, {"items": get_experience()}, None
        if name == "list_skills":
            return True, {"items": get_skills()}, None
        if name == "list_certifications":
            return True, get_certifications(), None
        if name == "get_availability":
            range_param = arguments.get("range")
            return True, filter_availability(range_param), None
        if name == "get_current_time_gmt7":
            # No arguments required
            return True, {"now": get_current_time_gmt7()}, None
        if name == "send_contact_message":
            required = ["name", "email", "message"]
            if any(not arguments.get(k) for k in required):
                return False, None, {"code": "ERR_BAD_REQUEST", "message": "name, email, message required"}
            ticket_id = await submit_contact_message(
                {
                    "name": arguments.get("name"),
                    "email": arguments.get("email"),
                    "message": arguments.get("message"),
                    "ip": None,
                }
            )
            return True, {"ticket_id": ticket_id}, None
        if name == "ask_portfolio_bot":
            question = arguments.get("question")
            if not question:
                return False, None, {"code": "ERR_BAD_REQUEST", "message": "Missing 'question'"}
            audience = arguments.get("audience") or "general"
            answer, sources, suggestions, events = answer_question(question, audience)
            return True, {
                "answer": answer,
                "sources": sources,
                "suggestions": suggestions,
                "events": events,
            }, None
        # Unknown tool
        return False, None, {"code": "ERR_NOT_FOUND", "message": f"Tool '{name}' not found"}
    except Exception as e:
        return False, None, {"code": "ERR_INTERNAL", "message": str(e)}


async def forward_jsonrpc_to_n8n(payload: Dict[str, Any]) -> Tuple[bool, bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Forward a raw JSON-RPC 2.0 payload to n8n if configured.
    If no webhook is configured, return a minimal valid JSON-RPC result for basic methods.

    Returns (ok, forwarded, json_response, error_message).
    """
    settings = get_settings()
    webhook = settings.n8n_mcp_webhook

    # If no webhook, provide a minimal local JSON-RPC fallback
    if not webhook:
        method = payload.get("method")
        req_id = payload.get("id")
        # Minimal handling of MCP lifecycle
        if method == "initialize":
            params = payload.get("params") or {}
            return True, False, {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": params.get("protocolVersion", "2025-03-26"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "Kane Portfolio MCP", "version": settings.app_version},
                },
            }, None
        if method == "tools/list":
            tools = _load_mcp_tools()
            return True, False, {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": tools},
            }, None
        if method == "tools/call":
            params = payload.get("params") or {}
            name = params.get("name")
            arguments = params.get("arguments") or {}
            ok, result, err = await _execute_local_tool(name, arguments)
            if not ok:
                # Map to JSON-RPC error codes
                code = -32602 if err and err.get("code") == "ERR_BAD_REQUEST" else -32601 if err and err.get("code") == "ERR_NOT_FOUND" else -32000
                return True, False, {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": code, "message": err.get("message") if err else "Tool call failed"},
                }, None
            # Format as MCP content array (text)
            try:
                import json as _json
                text_content = _json.dumps(result, ensure_ascii=False, default=str)
            except Exception:
                text_content = str(result)
            return True, False, {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": text_content}
                    ],
                    "isError": False,
                },
            }, None
        if method == "shutdown":
            return True, False, {"jsonrpc": "2.0", "id": req_id, "result": True}, None
        # Default: method not found
        return True, False, {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"},
        }, None

    # Webhook configured: pass-through
    try:
        async with httpx.AsyncClient(timeout=settings.n8n_mcp_timeout_seconds) as client:
            resp = await client.post(str(webhook), json=payload)
            resp.raise_for_status()
            # Return upstream JSON as-is if possible
            try:
                result = resp.json()
            except ValueError:
                # Not JSON; wrap as error-like payload
                result = {"jsonrpc": "2.0", "id": payload.get("id"), "error": {"code": -32001, "message": resp.text}}
            return True, True, result, None
    except httpx.HTTPError as e:
        return False, True, None, str(e)
