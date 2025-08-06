"""Application entrypoint initializing the FastAPI app and routers."""

from fastapi import FastAPI

from controllers.experience_controller import router as experience_router

app = FastAPI(title="My Career Storytelling")

# Register routers for experience endpoints.
app.include_router(experience_router)
