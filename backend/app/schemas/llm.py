from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class LLMBase(BaseModel):
    llm_model_name: str
    llm_vendor: str
    llm_type: str
    api_provider: str
    api_endpoint: str

class LLMCreate(LLMBase):
    pass

class LLMUpdate(LLMBase):
    pass

class LLMSchema(LLMBase):
    id: UUID

    class Config:
        from_attributes = True
