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

router = APIRouter()

@router.post(
    "/user/",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={
        200: {
            "description": "User created successfully",
        },
        400: {"description": "Bad request"},
        500: {"description": "Internal server error."}
    }
)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    print("Entra al endpoint")
    user_service = UserService(db=db)
    user = await user_service.create_user(user_create)
    if user.id is None:
        raise HTTPException(status_code=500, detail="User ID was not assigned")
    return user
    print("Resultado User Service: ", user)
    return user