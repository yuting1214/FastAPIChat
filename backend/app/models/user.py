import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.app.dependencies.database import Base
from backend.app.models.quota import user_quota_association_table

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip_address = Column(String, unique=True)
    name = Column(String, unique=True)

    # Relationships
    chats = relationship("Chat", back_populates="user")
    api_usages = relationship("APIUsage", back_populates="user")
    quotas = relationship("Quota", secondary=user_quota_association_table, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, ip_address={self.ip_address}, name={self.name})>"
