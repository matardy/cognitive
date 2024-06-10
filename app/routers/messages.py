from fastapi import APIRouter, Depends, HTTPException, status
from agents.BancoGuayaquil import ChatUserAgent
from schemas.message import ChatResponse, ChatRequest
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Union
from langsmith import traceable
from services.message_service import MessageService
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/message/",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful response with the large language model's output.",
        },
        400: {"description": "Invalid request due to incorrect data."},
        500: {"description": "Internal server error."}
    }
)
async def chat(chat_request: ChatRequest, session_id: str, conversation_id: int, db: AsyncSession = Depends(get_db)):
    message_service = MessageService(db=db, session_id=session_id)
    chat_response = await message_service.create_message(content=chat_request, conversation_id=conversation_id)
    return chat_response