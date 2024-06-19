from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from backend.app.dependencies.database import get_sync_db, get_async_db
from backend.app.models import Chat
from backend.app.schemas import ChatBase, ChatCreate

class ChatService:
    def __init__(self, db_sync: Session = Depends(get_sync_db), db_async: AsyncSession = Depends(get_async_db)):
        self.db_sync = db_sync
        self.db_async = db_async

    def create_chat(self, chat_data: ChatCreate) -> Chat:
        db_chat = Chat(**chat_data.model_dump())
        self.db_sync.add(db_chat)
        self.db_sync.commit()
        self.db_sync.refresh(db_chat)
        return db_chat
    
    async def create_chat_async(self, chat_data: ChatCreate) -> Chat:
        db_chat = Chat(**chat_data.model_dump())
        self.db_async.add(db_chat)
        await self.db_async.commit()
        await self.db_async.refresh(db_chat)
        return db_chat

    def get_chats(self, skip: int = 0, limit: int = 30) -> List[Chat]:
        return self.db_sync.query(Chat).offset(skip).limit(limit).all()

    def get_chat(self, chat_id: UUID) -> Chat:
        db_chat = self.db_sync.query(Chat).filter(Chat.id == chat_id).first()
        if db_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return db_chat

    def update_chat(self, chat_id: UUID, chat_data: ChatBase) -> Chat:
        db_chat = self.db_sync.query(Chat).filter(Chat.id == chat_id).first()
        if db_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        for key, value in chat_data.model_dump(exclude_unset=True).items():
            setattr(db_chat, key, value)
        self.db_sync.commit()
        self.db_sync.refresh(db_chat)
        return db_chat

    def delete_chat(self, chat_id: UUID) -> Chat:
        db_chat = self.db_sync.query(Chat).filter(Chat.id == chat_id).first()
        if db_chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        self.db_sync.delete(db_chat)
        self.db_sync.commit()
        return db_chat
