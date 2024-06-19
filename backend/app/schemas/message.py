from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class MessageBase(BaseModel):
    content: str
    message_type: str
    origin: str

class MessageCreate(MessageBase):
    chat_id: UUID

class MessageSchema(MessageBase):
    id: UUID
    chat_id: UUID

    class Config:
        from_attributes = True