from fastapi import FastAPI
from app.controllers.greeting import router as greeting_router

app = FastAPI()

app.include_router(greeting_router)
