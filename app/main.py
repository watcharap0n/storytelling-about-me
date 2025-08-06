"""Application entry point for the Storytelling API."""

from fastapi import FastAPI

from controllers.experience_controller import router as experience_router

app = FastAPI(title="My Career Storytelling")

# Register routers
app.include_router(experience_router)


@app.get("/")
async def root() -> dict:
    """Simple health check endpoint."""

    return {"status": "ok"}
