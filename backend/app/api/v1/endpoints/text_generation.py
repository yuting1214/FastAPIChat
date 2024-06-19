from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.app.dependencies.database import get_sync_db
from backend.app.models import (
    LLM,
    Quota,
    APIUsage,
    APICallDetail
)
from backend.app.models.quota import user_quota_association_table
from backend.app.schemas import LLMInput, LLMMemoryInput,LLMTextOutput
from llm.llm_text_chain import (
    llm_OpenRouter_chain,
    llm_OpenRouter_chain_stream,
    llm_OpenRouter_memory_chain_stream
)

router = APIRouter()

@router.post("/llm/generation/text", response_model=LLMTextOutput)
def chat_completion(chat_data: LLMInput, db: Session = Depends(get_sync_db)):
    # Fetch the data from the request
    current_user_id = chat_data.user_id
    endpoint = chat_data.api_endpoint
    prompt = chat_data.user_input
    is_arena = chat_data.is_arena

    # Fetch the llm_type based on api_endpoint
    llm = db.query(LLM).filter(LLM.api_endpoint == endpoint).first()
    if not llm:
        raise HTTPException(status_code=400, detail="Invalid API endpoint")
    
    # Check user's quota for the specific llm_type 
    quota_resource_type = 'Text_API' if llm.llm_type == 'text' else f'{llm.llm_type.capitalize()}_API'
    user_quota = db.query(Quota).join(user_quota_association_table).filter(
        user_quota_association_table.c.user_id == current_user_id,
        Quota.resource == quota_resource_type
    ).first()

    if not user_quota:
        raise HTTPException(status_code=400, detail="Quota not found for the user")
    
    # Get the user's API usage for the specific llm_type
    # usage_count = db.query(APIUsage).join(LLM).filter(
    #     APIUsage.user_id == current_user_id,
    #     LLM.llm_type == llm.llm_type
    # ).count()

    # # Check if the user has exceeded their quota
    # if usage_count >= user_quota.quota_limit:
    #     raise HTTPException(status_code=403, detail="Quota exceeded for the API endpoint")

    if (is_arena and user_quota.quota_limit < 2) or (not is_arena and user_quota.quota_limit < 1):
        raise HTTPException(status_code=403, detail="Quota limit reached")

    # Reduce the quota by one and update the database
    user_quota.quota_limit -= 1

    # Process the request if the quota has not been exceeded
    response_str = llm_OpenRouter_chain(prompt, endpoint)

    # Log the API usage
    api_usage = APIUsage(
        user_id=current_user_id,
        endpoint=endpoint
    )
    db.add(api_usage)
    db.commit()

    return {"response": response_str}

@router.post("/llm/generation/stream/text", response_model=LLMTextOutput)
def chat_completion_stream(chat_data: LLMInput, db: Session = Depends(get_sync_db)):
    # Fetch the data from the request
    current_user_id = chat_data.user_id
    chat_id = chat_data.chat_id
    endpoint = chat_data.api_endpoint
    user_input = chat_data.user_input
    is_arena = chat_data.is_arena
    llm_label = chat_data.llm_label
    llm_params = chat_data.llm_params.model_dump()

    # Fetch the llm based on api_endpoint
    llm = db.query(LLM).filter(LLM.api_endpoint == endpoint).first()
    if not llm:
        raise HTTPException(status_code=400, detail="Invalid API endpoint")

    # Check user's quota for the specific llm_type 
    quota_resource_type = 'Text_API' if llm.llm_type == 'text' else f'{llm.llm_type.capitalize()}_API'
    user_quota = db.query(Quota).join(user_quota_association_table).filter(
        user_quota_association_table.c.user_id == current_user_id,
        Quota.resource == quota_resource_type
    ).first()

    if not user_quota:
        raise HTTPException(status_code=400, detail="Quota not found for the user")
    
    if (is_arena and user_quota.quota_limit < 2) or (not is_arena and user_quota.quota_limit < 1):
        raise HTTPException(status_code=403, detail="Quota limit reached")

    # Reduce the quota by one and update the database
    user_quota.quota_limit -= 1
    db.commit()  # Commit the quota change before starting the response stream

    # Log the API usage
    api_usage = APIUsage(
        user_id=current_user_id,
        chat_id=chat_id,
        llm_label=llm_label,
        endpoint=endpoint,
    )
    db.add(api_usage)
    db.commit()

    # Log the API Detail
    api_calldetail = APICallDetail(
        api_usage_id=api_usage.id,
        system_prompt=llm_params["system_prompt"],
        temperature=llm_params["temperature"],
        top_p=llm_params["top_p"]
    )
    db.add(api_calldetail)
    db.commit()
    
    # Use the streaming generator function directly
    return StreamingResponse(
        llm_OpenRouter_chain_stream(user_input, endpoint, llm_params),
        media_type="text/plain")

@router.post("/llm/generation/stream/text/memory", response_model=LLMTextOutput)
def chat_completion_memory_stream(chat_data: LLMMemoryInput, db: Session = Depends(get_sync_db)):
    # Fetch the data from the request
    current_user_id = chat_data.user_id
    chat_id = chat_data.chat_id
    endpoint = chat_data.api_endpoint
    user_input = chat_data.user_input
    is_arena = chat_data.is_arena
    llm_label = chat_data.llm_label
    llm_params = chat_data.llm_params.model_dump()
    formated_history = chat_data.formated_history

    # Fetch the llm based on api_endpoint
    llm = db.query(LLM).filter(LLM.api_endpoint == endpoint).first()
    if not llm:
        raise HTTPException(status_code=400, detail="Invalid API endpoint")

    # Check user's quota for the specific llm_type 
    quota_resource_type = 'Text_API' if llm.llm_type == 'text' else f'{llm.llm_type.capitalize()}_API'
    user_quota = db.query(Quota).join(user_quota_association_table).filter(
        user_quota_association_table.c.user_id == current_user_id,
        Quota.resource == quota_resource_type
    ).first()

    if not user_quota:
        raise HTTPException(status_code=400, detail="Quota not found for the user")
    
    if (is_arena and user_quota.quota_limit < 2) or (not is_arena and user_quota.quota_limit < 1):
        raise HTTPException(status_code=403, detail="Quota limit reached")

    # Reduce the quota by one and update the database
    user_quota.quota_limit -= 1
    db.commit()  # Commit the quota change before starting the response stream

    # Log the API usage
    api_usage = APIUsage(
        user_id=current_user_id,
        chat_id=chat_id,
        llm_label=llm_label,
        endpoint=endpoint,
    )
    db.add(api_usage)
    db.commit()

    # Log the API Detail
    api_calldetail = APICallDetail(
        api_usage_id=api_usage.id,
        system_prompt=llm_params["system_prompt"],
        temperature=llm_params["temperature"],
        top_p=llm_params["top_p"]
    )
    db.add(api_calldetail)
    db.commit()
    
    # Use the streaming generator function directly
    return StreamingResponse(
        llm_OpenRouter_memory_chain_stream(user_input, endpoint, llm_params, formated_history),
        media_type="text/plain")