import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.dependencies.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    #chat_history_id = Column(UUID(as_uuid=True), ForeignKey('chat_history.id'))
    mode = Column(ENUM('chat', 'arena', 'image', name='chat_mode'))
    timestamp = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")
    rating = relationship("Rating", uselist=False, back_populates="chat")
    api_usages = relationship("APIUsage", back_populates="chat")
    #chat_history = relationship("ChatHistory", back_populates="chats")

    def __repr__(self):
        return f"<Chat(id={self.id}, start_time={self.start_time}, end_time={self.end_time})>"
