"""Application entry point for the career storytelling API."""

from fastapi import FastAPI

from app.controllers.experience_controller import router as experience_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(title="My Career Storytelling API", version="1.0.0")
    app.include_router(experience_router)
    return app


app = create_app()


if __name__ == "__main__":
    # Allows running the app with `python app/main.py`
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
