from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"))
    user = relationship("User", back_populates="conversations", lazy='selectin')
    messages = relationship("Message", back_populates="conversation", lazy='selectin')