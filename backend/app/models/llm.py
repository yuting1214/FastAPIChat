import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from backend.app.dependencies.database import Base
from sqlalchemy.orm import relationship

class LLM(Base):
    __tablename__ = 'llms'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    llm_model_name = Column(String(100), nullable=False) 
    llm_vendor = Column(String(100), nullable=False)
    llm_type = Column(ENUM('text', 'image', 'audio', 'multi', name='llm_type'), nullable=False) 
    api_provider = Column(String(100), nullable=False)
    api_endpoint = Column(Text, nullable=False, unique=True)

    # Relationship
    api_usages = relationship("APIUsage", back_populates="llm")

    def __repr__(self):
        return (f"<LLM(id='{self.id}', llm_model_name='{self.llm_model_name}', llm_vendor='{self.llm_vendor}', "
                f"llm_type='{self.llm_type}', api_provider='{self.api_provider}', api_endpoint='{self.api_endpoint}',")