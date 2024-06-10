from fastapi import APIRouter, Depends, HTTPException, status
from agents.BancoGuayaquil import ChatUserAgent
from schemas.message import ChatResponse, ChatRequest
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Union
from langsmith import traceable
from services.message_service import MessageService
from core.database import get_db
from sqlalchemy.orm import Session
from schemas.user import User, UserCreate
from services.user_service import UserService
from schemas.conversation import Conversation, ConversationCreate
from services.conversation_service import ConversationService
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.post(
    "/conversation/",
    status_code=status.HTTP_200_OK,
    response_model=Conversation,
    responses={
        200: {
            "description": "Conversation created successfully",
        },
        400: {"description": "Bad request"},
        500: {"description": "Internal server error."}
    }
)
async def create_conversation(conversation_create: ConversationCreate, db: AsyncSession = Depends(get_db)):
    conversation_service = ConversationService(db=db)
    conversation = await conversation_service.create_conversation(conversation_create.user_id)
    return conversation

@router.get(
    "/conversation/{conversation_id}",
    status_code=status.HTTP_200_OK,
    response_model=Conversation,
    responses={
        200: {
            "description": "Conversation retrieved successfully",
        },
        404: {"description": "Conversation not found"},
        500: {"description": "Internal server error."}
    }
)
async def get_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    conversation_service = ConversationService(db=db)
    conversation = await conversation_service.get_conversation_by_id(conversation_id)
    return conversation