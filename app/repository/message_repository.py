from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Session
from models.message import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_message(self, content: str, role: str, conversation_id: int) -> Message:
        message = Message(content=content, role=role, conversation_id=conversation_id)
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message