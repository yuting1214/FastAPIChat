from typing import Optional, List, Dict, Tuple
from uuid import UUID
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from langchain.memory import ConversationBufferWindowMemory

class LLMParams(BaseModel):
    system_prompt: str
    temperature: Annotated[float, Field(strict=True, ge=0.0, le=2.0)]
    top_p: Annotated[float, Field(strict=True, ge=0.0, le=1.0)]

class LLMInput(BaseModel):
    user_id: UUID
    chat_id: UUID
    api_endpoint: str
    user_input: str
    is_arena: bool
    llm_label: str = None
    llm_params: LLMParams

class LLMMemoryInput(LLMInput):
    formated_history: List[Tuple[str, str]]

class LLMTextOutput(BaseModel):
    response: str

class LLMImageOutput(BaseModel):
    image_url: str