"""FastAPI application entry point."""
from fastapi import FastAPI
from controllers.experience_controller import router as experience_router

# Create FastAPI application
app = FastAPI(title="Career Storytelling API")

# Register routers
app.include_router(experience_router)
