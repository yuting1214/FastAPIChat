import uuid
from sqlalchemy import Column, Text, Float, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.dependencies.database import Base

class APICallDetail(Base):
    __tablename__ = 'api_call_detail'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_usage_id = Column(UUID(as_uuid=True), ForeignKey('api_usages.id'), unique=True)
    system_prompt = Column(Text, nullable=False)
    temperature = Column(Float, nullable=False, default=1.0)
    top_p = Column(Float, nullable=False, default=1.0)

    api_usage = relationship("APIUsage", back_populates="call_detail")