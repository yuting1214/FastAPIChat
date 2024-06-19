import uuid
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from backend.app.dependencies.database import Base

user_quota_association_table = Table(
    "user_quota_association",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("quota_id", UUID(as_uuid=True), ForeignKey("quotas.id"), primary_key=True)
)

class Quota(Base):
    __tablename__ = "quotas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource = Column(ENUM('Text_API', 'Image_API', 'Storage_API', name='resource_types'))
    quota_limit = Column(Integer, default=10) 

    # Relationships
    users = relationship("User", secondary=user_quota_association_table, back_populates="quotas")

    def __repr__(self):
        return f"<Quota(id={self.id}, resource={self.resource}, quota_limit={self.quota_limit})>"