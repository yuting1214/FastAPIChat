from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from backend.app.dependencies.database import get_sync_db
from backend.app.models import Rating
from backend.app.schemas import RatingBase, RatingCreate

class RatingService:
    def __init__(self, db: Session = Depends(get_sync_db)):
        self.db = db

    def create_rating(self, rating_data: RatingCreate) -> Rating:
        db_rating = Rating(**rating_data.model_dump())
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    def get_ratings(self, skip: int = 0, limit: int = 30) -> List[Rating]:
        return self.db.query(Rating).offset(skip).limit(limit).all()

    def get_rating(self, rating_id: UUID) -> Rating:
        db_rating = self.db.query(Rating).filter(Rating.id == rating_id).first()
        if db_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found")
        return db_rating

    def update_rating(self, rating_id: UUID, rating_data: RatingBase) -> Rating:
        db_rating = self.db.query(Rating).filter(Rating.id == rating_id).first()
        if db_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found")
        for key, value in rating_data.model_dump(exclude_unset=True).items():
            setattr(db_rating, key, value)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    def delete_rating(self, rating_id: UUID) -> Rating:
        db_rating = self.db.query(Rating).filter(Rating.id == rating_id).first()
        if db_rating is None:
            raise HTTPException(status_code=404, detail="Rating not found")
        self.db.delete(db_rating)
        self.db.commit()
        return db_rating
