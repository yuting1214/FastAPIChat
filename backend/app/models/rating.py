import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from backend.app.dependencies.database import Base

class Rating(Base):
    __tablename__ = "rating"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chats.id'))
    rating_type = Column(ENUM('upvote', 'downvote', 'model_1_better', 'model_2_better', 'tie', 'both_bad', name='rating_type'))
    comment = Column(String)

    # Relationships
    chat = relationship("Chat", uselist=False, back_populates="rating")

    def __repr__(self):
        return f"<Rating(id={self.id}, chat_id={self.chat_id}, rating_type={self.rating_type}, comment={self.comment})>"
