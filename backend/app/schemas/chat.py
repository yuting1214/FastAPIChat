from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ChatBase(BaseModel):
    pass

class ChatCreate(BaseModel):
    mode: str
    user_id: UUID

class ChatSchema(ChatBase):
    id: UUID
    user_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True