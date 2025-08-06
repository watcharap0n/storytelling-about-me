from fastapi import APIRouter
from app.services.greeting import create_message
from app.models.message import Message

router = APIRouter(prefix="/greeting", tags=["greeting"])

@router.get("/", response_model=Message)
def read_greeting() -> Message:
    return Message(message=create_message())
