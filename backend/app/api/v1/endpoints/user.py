from typing import List
from names_generator import generate_name
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.dependencies.database import get_sync_db
from backend.app.models import User
from backend.app.schemas import UserSchema, UserCreate

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
async def create_user(user_data: UserCreate, db: Session = Depends(get_sync_db)):
    # Check if the user already exists with the given IP address
    existing_user = db.query(User).filter(User.ip_address == user_data.ip_address).first()
    if existing_user:
        return existing_user

    # Generate a unique human-readable name
    unique_name = generate_name()

    # Create a new user
    new_user = User(**user_data.model_dump(), name=unique_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/", response_model=List[UserSchema])
async def get_users(skip: int = 0, limit: int = 30, db: Session = Depends(get_sync_db)):
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str, db: Session = Depends(get_sync_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/ip/{ip_address}", response_model=UserSchema)
async def get_user_by_ip(ip_address: str, db: Session = Depends(get_sync_db)):
    db_user = db.query(User).filter(User.ip_address == ip_address).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user