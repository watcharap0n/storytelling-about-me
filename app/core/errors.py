"""Error handling utilities for consistent error responses."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


ERROR_STATUS_MAP = {
    400: "ERR_BAD_REQUEST",
    401: "ERR_AUTH",
    403: "ERR_AUTH",
    404: "ERR_NOT_FOUND",
    429: "ERR_RATE_LIMIT",
    500: "ERR_INTERNAL",
    502: "ERR_UPSTREAM",
}


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, dict) else {"message": exc.detail}
        code = detail.get("code") or ERROR_STATUS_MAP.get(exc.status_code, "ERR_INTERNAL")
        correlation_id = detail.get("correlation_id")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": code,
                    "message": detail.get("message", ""),
                    "correlation_id": correlation_id,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        correlation_id = getattr(request.state, "correlation_id", None)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "ERR_INTERNAL",
                    "message": "An unexpected error occurred.",
                    "correlation_id": correlation_id,
                }
            },
        )
