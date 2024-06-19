from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from backend.app.crud import ChatService
from backend.app.schemas import ChatBase, ChatCreate, ChatSchema

router = APIRouter()

@router.post("/chats/", response_model=ChatSchema)
def create_chat(chat_data: ChatCreate, service: ChatService = Depends()):
    return service.create_chat(chat_data)

@router.post("/chats/async", response_model=ChatSchema)
async def create_chat_async(chat_data: ChatCreate, service: ChatService = Depends()):
    return await service.create_chat_async(chat_data)

@router.get("/chats/", response_model=List[ChatSchema])
def get_chats(skip: int = 0, limit: int = 30, service: ChatService = Depends()):
    return service.get_chats(skip, limit)

@router.get("/chats/{chat_id}", response_model=ChatSchema)
def get_chat(chat_id: UUID, service: ChatService = Depends()):
    return service.get_chat(chat_id)

@router.put("/chats/{chat_id}", response_model=ChatSchema)
def update_chat(chat_id: UUID, chat_data: ChatBase, service: ChatService = Depends()):
    return service.update_chat(chat_id, chat_data)

@router.delete("/chats/{chat_id}", response_model=ChatSchema)
def delete_chat(chat_id: UUID, service: ChatService = Depends()):
    return service.delete_chat(chat_id)
