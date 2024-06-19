from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    ip_address: str

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: UUID
    name: str

    class Config:
        from_attributes = True