from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from backend.app.crud import MessageService
from backend.app.schemas import (
    MessageBase,
    MessageCreate,
    MessageSchema
)

router = APIRouter()

@router.post("/messages/", response_model=MessageSchema)
def create_message(message_data: MessageCreate, service: MessageService = Depends()):
    return service.create_message(message_data)

@router.post("/messages/async", response_model=MessageSchema)
async def create_message_async(message_data: MessageCreate, service: MessageService = Depends()):
    return await service.create_message_async(message_data)

@router.get("/messages/", response_model=List[MessageSchema])
def get_messages(skip: int = 0, limit: int = 30, service: MessageService = Depends()):
    return service.get_messages(skip, limit)

@router.get("/messages/{message_id}", response_model=MessageSchema)
def get_message(message_id: UUID, service: MessageService = Depends()):
    return service.get_message(message_id)

@router.put("/messages/{message_id}", response_model=MessageSchema)
def update_message(message_id: UUID, message_data: MessageBase, service: MessageService = Depends()):
    return service.update_message(message_id, message_data)

@router.delete("/messages/{message_id}", response_model=MessageSchema)
def delete_message(message_id: UUID, service: MessageService = Depends()):
    return service.delete_message(message_id)