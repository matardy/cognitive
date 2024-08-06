from repository.message_repository import MessageRepository
from agents.aws_agent import ChatUserAgent
from schemas.message import ChatRequest, ChatResponse, HumanMessage,AIMessage
from sqlalchemy.ext.asyncio import AsyncSession
from utils.utils  import encrypt_message, decrypt_message
from dotenv import load_dotenv
import os
load_dotenv
SECRET_DB_KEY = os.getenv('SECRET_DB_KEY')

class MessageService:
    def __init__(self, db: AsyncSession, session_id: str):
        self.message_repository = MessageRepository(db)
        self.session_id = session_id

    async def create_message(self, content: ChatRequest, conversation_id: int) -> ChatResponse:
        # Guardar el mensaje del usuario encriptado
        encrypted_content = encrypt_message(content.message, SECRET_DB_KEY)
        await self.message_repository.create_message(content=encrypted_content, role="human", conversation_id=conversation_id)

        # Obtener la respuesta del agente
        chat_agent = ChatUserAgent(enable_memory=True, session_id=self.session_id)
        ai_response = chat_agent.run(input=content.message)
        print("AI RESPONSE: ", ai_response)
        print('output: ', ai_response.get('output'))

        # Guardar la respuesta del AI encriptada
        encrypted_ai_response = encrypt_message(str(ai_response.get('output')), SECRET_DB_KEY)
        await self.message_repository.create_message(content=encrypted_ai_response, role="ai", conversation_id=conversation_id)

        # Convertir chat_history a diccionarios
        chat_history = []
        for msg in ai_response.get('chat_history', []):
            if isinstance(msg, HumanMessage):
                chat_history.append(HumanMessage(content=msg.content).dict())
            elif isinstance(msg, AIMessage):
                chat_history.append(AIMessage(content=msg.content).dict())

        # Crear y devolver la respuesta del chat
        chat_response = ChatResponse(
            input=content.message,
            chat_history=chat_history,
            output=ai_response.get('output')
        )

        return chat_response