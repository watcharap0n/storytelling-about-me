"""Chat/FAQ endpoint."""

from fastapi import APIRouter, Depends

from app.core.middleware import verify_api_key
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import answer_question

router = APIRouter(prefix="/v1/chat", tags=["Chat"], dependencies=[Depends(verify_api_key)])


@router.post("/ask", response_model=ChatResponse)
async def ask_portfolio_bot(payload: ChatRequest) -> ChatResponse:
    answer, sources, suggestions, events = answer_question(payload.question, payload.audience or "general")
    return ChatResponse(answer=answer, sources=sources, suggestions=suggestions, events=events)
