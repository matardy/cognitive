from pydantic import BaseModel
from typing import List, Union
from pydantic import BaseModel, Field


""" Schemas to handle indivuals responses related to LLM interactions """
class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        description="The message text to be processed by the large language model.",
        example="Hello, how are you AI Assistant?"
    )
class HumanMessage(BaseModel):
    content: str = Field(..., description="Text of the message sent by a human.")

class AIMessage(BaseModel):
    content: str = Field(..., description="Text of the message generated by the AI.")

class ChatResponse(BaseModel):
    input: str = Field(
        ...,
        description="The user's input message to the system.",
        example="How are you?"
    )
    chat_history: List[Union[HumanMessage, AIMessage]] = Field(
        default=[],
        description="The history of the chat session, consisting of messages from both the human user and AI responses.",
        example=[]
    )
    output: str = Field(
        ...,
        description="The processed response from the large language model.",
        example="Im good."
    )

""" Schemas to handle Message Database Object """
class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    conversation_id: int

    class Config:
        orm_mode = True