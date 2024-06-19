from typing_extensions import Annotated
from pydantic import BaseModel, Field
from uuid import UUID

class APICallDetailBase(BaseModel):
    api_usage_id: UUID
    system_prompt: str
    temperature: Annotated[float, Field(strict=True, ge=0.0, le=2.0)]
    top_p: Annotated[float, Field(strict=True, ge=0.0, le=1.0)]

class APICallDetailCreate(APICallDetailBase):
    pass

class APICallDetailSchema(APICallDetailBase):
    id: UUID

    class Config:
        from_attributes = True
