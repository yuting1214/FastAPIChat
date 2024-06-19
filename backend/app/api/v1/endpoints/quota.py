from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.dependencies.database import get_sync_db
from backend.app.models import Quota, User
from backend.app.schemas import QuotaSchema, QuotaCreate, QuotaUpdate

router = APIRouter()

@router.post("/quotas/", response_model=QuotaSchema)
def create_quota(quota_data: QuotaCreate, db: Session = Depends(get_sync_db)):
    # Initialize quota_dict from quota_data
    quota_dict = quota_data.model_dump()
    
    # Check if users list is not empty
    if quota_data.users:
        # Fetch the User instances from the database
        user_ids = [user.id for user in quota_data.users]
        users = db.query(User).filter(User.id.in_(user_ids)).all()

        # Check if all user IDs were found
        if len(users) != len(user_ids):
            raise HTTPException(status_code=404, detail="One or more users not found")

        # Replace users list with the fetched User instances
        quota_dict['users'] = users
    else:
        # Assign an empty list to users
        quota_dict['users'] = []

    # Create a Quota instance
    db_quota = Quota(**quota_dict)
    
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota

@router.get("/quotas/{quota_id}", response_model=QuotaSchema)
def read_quota(quota_id: UUID, db: Session = Depends(get_sync_db)):
    db_quota = db.query(Quota).filter(Quota.id == quota_id).first()
    if db_quota is None:
        raise HTTPException(status_code=404, detail="QuotaSchema not found")
    return db_quota

@router.put("/quotas/{quota_id}", response_model=QuotaSchema)
def update_quota(quota_id: UUID, quota_data: QuotaUpdate, db: Session = Depends(get_sync_db)):
    db_quota = db.query(Quota).filter(Quota.id == quota_id).first()
    if db_quota is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    for key, value in quota_data.model_dump().items():
        setattr(db_quota, key, value)
    db.commit()
    db.refresh(db_quota)
    return db_quota

@router.delete("/quotas/{quota_id}", response_model=QuotaSchema)
def remove_quota(quota_id: UUID, db: Session = Depends(get_sync_db)):
    db_quota = db.query(Quota).filter(Quota.id == quota_id).first()
    if db_quota is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    db.delete(db_quota)
    db.commit()
    return db_quota

