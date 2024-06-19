import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.dependencies.database import Base

class APIUsage(Base):
    __tablename__ = "api_usages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chats.id'))
    timestamp = Column(DateTime, default=func.now())
    endpoint = Column(String, ForeignKey('llms.api_endpoint'))
    llm_label = Column(ENUM('model_1', 'model_2', name='llm_identifier'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="api_usages")
    chat = relationship("Chat", back_populates="api_usages")
    llm = relationship("LLM", back_populates="api_usages")
    call_detail = relationship("APICallDetail", uselist=False, back_populates="api_usage")

    def __repr__(self):
        return f"<APIUsage(id={self.id}, user_id={self.user_id}, chat_id={self.chat_id}, timestamp={self.timestamp}, endpoint={self.endpoint}, mode={self.mode})>"

