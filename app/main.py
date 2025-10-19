"""Application entry point for Kane's portfolio API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.about_controller import router as about_router
from app.controllers.pillars_controller import router as pillars_router
from app.controllers.work_controller import router as work_router
from app.controllers.experience_controller import router as experience_router
from app.controllers.skills_controller import router as skills_router
from app.controllers.certifications_controller import router as certifications_router
from app.controllers.contact_controller import router as contact_router
from app.controllers.availability_controller import router as availability_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.system_controller import router as system_router
from app.controllers.mcp_controller import router as mcp_router
from app.controllers.time_controller import router as time_router
from app.core.config import get_settings
from app.core.errors import setup_exception_handlers
from app.core.middleware import CorrelationIdMiddleware, LoggingMiddleware, RateLimitMiddleware
from app.core.cors import enforce_post_cors


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url=None,
    )

    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"]
    )

    app.middleware("http")(enforce_post_cors)

    setup_exception_handlers(app)

    app.include_router(system_router)
    app.include_router(about_router)
    app.include_router(pillars_router)
    app.include_router(work_router)
    app.include_router(experience_router)
    app.include_router(skills_router)
    app.include_router(certifications_router)
    app.include_router(contact_router)
    app.include_router(availability_router)
    app.include_router(chat_router)
    app.include_router(mcp_router)
    app.include_router(time_router)

    return app


app = create_app()
