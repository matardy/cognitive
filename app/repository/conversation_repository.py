from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.conversation import Conversation
from models.user import User
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload, Session

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db 

    async def create_conversation(self, user_id: str) -> Conversation:
        # Verificar si el usuario existe
        result = self.db.execute(select(User).filter(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
        
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    async def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        result = self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .filter(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

        # Validar que todos los mensajes tengan contenido
        for message in conversation.messages:
            if message.content is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Message content is missing")
        
        return conversation