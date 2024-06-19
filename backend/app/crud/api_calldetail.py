from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from backend.app.dependencies.database import get_sync_db, get_async_db
from backend.app.models import APICallDetail
from backend.app.schemas import APICallDetailBase, APICallDetailCreate

class APICallDetailService:
    def __init__(self, db_sync: Session = Depends(get_sync_db), db_async: AsyncSession = Depends(get_async_db)):
        self.db_sync = db_sync
        self.db_async = db_async

    def create_api_call_detail(self, api_call_detail_data: APICallDetailCreate) -> APICallDetail:
        db_api_call_detail = APICallDetail(**api_call_detail_data.dict())
        self.db_sync.add(db_api_call_detail)
        self.db_sync.commit()
        self.db_sync.refresh(db_api_call_detail)
        return db_api_call_detail
    
    async def create_api_call_detail_async(self, api_call_detail_data: APICallDetailCreate) -> APICallDetail:
        db_api_call_detail = APICallDetail(**api_call_detail_data.dict())
        self.db_async.add(db_api_call_detail)
        await self.db_async.commit()
        await self.db_async.refresh(db_api_call_detail)
        return db_api_call_detail

    def get_api_call_details(self, skip: int = 0, limit: int = 30) -> List[APICallDetail]:
        return self.db_sync.query(APICallDetail).offset(skip).limit(limit).all()

    def get_api_call_detail(self, api_call_detail_id: UUID) -> APICallDetail:
        db_api_call_detail = self.db_sync.query(APICallDetail).filter(APICallDetail.id == api_call_detail_id).first()
        if db_api_call_detail is None:
            raise HTTPException(status_code=404, detail="API Call Detail not found")
        return db_api_call_detail

    def update_api_call_detail(self, api_call_detail_id: UUID, api_call_detail_data: APICallDetailBase) -> APICallDetail:
        db_api_call_detail = self.db_sync.query(APICallDetail).filter(APICallDetail.id == api_call_detail_id).first()
        if db_api_call_detail is None:
            raise HTTPException(status_code=404, detail="API Call Detail not found")
        for key, value in api_call_detail_data.dict(exclude_unset=True).items():
            setattr(db_api_call_detail, key, value)
        self.db_sync.commit()
        self.db_sync.refresh(db_api_call_detail)
        return db_api_call_detail

    def delete_api_call_detail(self, api_call_detail_id: UUID) -> APICallDetail:
        db_api_call_detail = self.db_sync.query(APICallDetail).filter(APICallDetail.id == api_call_detail_id).first()
        if db_api_call_detail is None:
            raise HTTPException(status_code=404, detail="API Call Detail not found")
        self.db_sync.delete(db_api_call_detail)
        self.db_sync.commit()
        return db_api_call_detail
