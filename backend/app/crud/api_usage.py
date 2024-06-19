from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from backend.app.dependencies.database import get_sync_db, get_async_db
from backend.app.models import APIUsage
from backend.app.schemas import APIUsageBase, APIUsageCreate, APIUsageSchema

class APIUsageService:
    def __init__(self, db_sync: Session = Depends(get_sync_db), db_async: AsyncSession = Depends(get_async_db)):
        self.db_sync = db_sync
        self.db_async = db_async

    def create_api_usage(self, api_usage_data: APIUsageCreate) -> APIUsage:
        db_api_usage = APIUsage(**api_usage_data.model_dump())
        self.db_sync.add(db_api_usage)
        self.db_sync.commit()
        self.db_sync.refresh(db_api_usage)
        return db_api_usage
    
    async def create_api_usage_async(self, api_usage_data: APIUsageCreate) -> APIUsage:
        db_api_usage = APIUsage(**api_usage_data.model_dump())
        self.db_async.add(db_api_usage)
        await self.db_async.commit()
        await self.db_async.refresh(db_api_usage)
        return db_api_usage

    def get_api_usages(self, skip: int = 0, limit: int = 30) -> List[APIUsage]:
        return self.db_sync.query(APIUsage).offset(skip).limit(limit).all()

    def get_api_usage(self, api_usage_id: UUID) -> APIUsage:
        db_api_usage = self.db_sync.query(APIUsage).filter(APIUsage.id == api_usage_id).first()
        if db_api_usage is None:
            raise HTTPException(status_code=404, detail="API Usage not found")
        return db_api_usage

    def update_api_usage(self, api_usage_id: UUID, api_usage_data: APIUsageBase) -> APIUsage:
        db_api_usage = self.db_sync.query(APIUsage).filter(APIUsage.id == api_usage_id).first()
        if db_api_usage is None:
            raise HTTPException(status_code=404, detail="API Usage not found")
        for key, value in api_usage_data.model_dump(exclude_unset=True).items():
            setattr(db_api_usage, key, value)
        self.db_sync.commit()
        self.db_sync.refresh(db_api_usage)
        return db_api_usage

    def delete_api_usage(self, api_usage_id: UUID) -> APIUsage:
        db_api_usage = self.db_sync.query(APIUsage).filter(APIUsage.id == api_usage_id).first()
        if db_api_usage is None:
            raise HTTPException(status_code=404, detail="API Usage not found")
        self.db_sync.delete(db_api_usage)
        self.db_sync.commit()
        return db_api_usage
