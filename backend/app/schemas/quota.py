from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from enum import Enum
import uuid


class UserQuataBase(BaseModel):
    id: UUID

class ResourceEnum(str, Enum):
    Text_API = "Text_API"
    Image_API = "Image_API"
    Storage = "Storage"

class QuotaBase(BaseModel):
    resource: ResourceEnum
    quota_limit: int

class QuotaCreate(QuotaBase):
    users: List[UserQuataBase] = []

class QuotaUpdate(QuotaBase):
    pass

class QuotaSchema(QuotaBase):
    id: UUID
    users: List[UserQuataBase] = []

    class Config:
        from_attributes = True
