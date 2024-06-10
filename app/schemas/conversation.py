from pydantic import BaseModel
from typing import List
from .message import Message

class ConversationBase(BaseModel):
    user_id: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    messages: List[Message] = []

    class Config:
        orm_mode = True
