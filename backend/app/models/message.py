import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from backend.app.dependencies.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chats.id'))
    content = Column(String)
    message_type = Column(ENUM('text', 'image', name='message_type'), nullable=False) 
    origin = Column(ENUM('user', 'model', name='origin'), nullable=False)

    # Relationships
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, content={self.content}, message_type={self.message_type}, origin={self.origin})>"