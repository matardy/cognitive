

from sqlalchemy.ext.asyncio import AsyncSession
from models.conversation import Conversation
from repository.conversation_repository import ConversationRepository
from typing import List

class ConversationService:
    def __init__(self, db: AsyncSession):
        self.conversation_repository = ConversationRepository(db)
        self.db = db 

    async def create_conversation(self, user_id: str) -> Conversation:
        return await self.conversation_repository.create_conversation(user_id=user_id)

    async def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        return await self.conversation_repository.get_conversation_by_id(conversation_id)