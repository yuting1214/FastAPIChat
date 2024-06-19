from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class RatingBase(BaseModel):
    rating_type: str
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    chat_id: UUID

class RatingSchema(RatingBase):
    id: UUID
    chat_id: UUID

    class Config:
        from_attributes = True
