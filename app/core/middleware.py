"""Custom middleware and dependencies for the API."""

import time
import uuid
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException

from app.core.config import get_settings


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID to each request and response."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["x-correlation-id"] = correlation_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Simple structured logging for requests."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.time()
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration = (time.time() - start) * 1000
            correlation_id = getattr(request.state, "correlation_id", "-")
            status = response.status_code if response else 500
            log_message = (
                f"method={request.method} path={request.url.path} status={status} "
                f"duration_ms={duration:.2f} correlation_id={correlation_id}"
            )
            print(log_message)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory rate limiting per client IP address."""

    def __init__(self, app):
        super().__init__(app)
        settings = get_settings()
        self.limit = settings.rate_limit_per_minute
        self._store: dict[str, tuple[int, float]] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = int(now // 60)
        key = f"{client_ip}:{window}"
        count, _ = self._store.get(key, (0, now))
        count += 1
        if count > self.limit:
            retry_after = 60 - (now % 60)
            correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "ERR_RATE_LIMIT",
                        "message": "Rate limit exceeded. Try again shortly.",
                        "correlation_id": correlation_id,
                    }
                },
                headers={"Retry-After": f"{int(retry_after)}"},
            )
        self._store[key] = (count, now)
        response = await call_next(request)
        return response


async def verify_api_key(request: Request) -> None:
    """Dependency to enforce x-api-key header."""

    if request.url.path.startswith("/healthz") or request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return
    if request.method == "OPTIONS":
        return
    api_key_header = request.headers.get("x-api-key")
    settings = get_settings()
    if not api_key_header or api_key_header != settings.api_key:
        correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))
        raise HTTPException(
            status_code=401,
            detail={
                "code": "ERR_AUTH",
                "message": "Invalid or missing API key.",
                "correlation_id": correlation_id,
            },
        )
