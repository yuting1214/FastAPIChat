from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class APIUsageBase(BaseModel):
    user_id: UUID
    chat_id: UUID
    endpoint: str

class APIUsageCreate(APIUsageBase):
    llm_label: Optional[str] = None

class APIUsageSchema(APIUsageBase):
    id: UUID
    timestamp: datetime
    llm_label: Optional[str] = None

    class Config:
        from_attributes = True
