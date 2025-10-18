"""CORS configuration helpers."""

from typing import Callable

from fastapi import Request
from starlette.responses import JSONResponse

ALLOWED_POST_PATHS = {"/v1/contact/message", "/v1/chat/ask", "/v1/mcp/execute"}


async def enforce_post_cors(request: Request, call_next: Callable):
    if request.method == "POST":
        origin = request.headers.get("origin")
        if origin and request.url.path not in ALLOWED_POST_PATHS:
            return JSONResponse(
                status_code=405,
                content={
                    "error": {
                        "code": "ERR_BAD_REQUEST",
                        "message": "Cross-origin POST not permitted for this endpoint.",
                        "correlation_id": getattr(request.state, "correlation_id", None),
                    }
                },
            )
    return await call_next(request)
