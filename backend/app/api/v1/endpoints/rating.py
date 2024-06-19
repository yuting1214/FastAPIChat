from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from backend.app.crud import RatingService
from backend.app.schemas import RatingBase, RatingCreate, RatingSchema

router = APIRouter()

@router.post("/ratings/", response_model=RatingSchema)
def create_rating(rating_data: RatingCreate, service: RatingService = Depends()):
    return service.create_rating(rating_data)

@router.post("/ratings/async", response_model=RatingSchema)
async def create_rating_async(rating_data: RatingCreate, service: RatingService = Depends()):
    return await service.create_rating_async(rating_data)

@router.get("/ratings/", response_model=List[RatingSchema])
def get_ratings(skip: int = 0, limit: int = 30, service: RatingService = Depends()):
    return service.get_ratings(skip, limit)

@router.get("/ratings/{rating_id}", response_model=RatingSchema)
def get_rating(rating_id: UUID, service: RatingService = Depends()):
    return service.get_rating(rating_id)

@router.put("/ratings/{rating_id}", response_model=RatingSchema)
def update_rating(rating_id: UUID, rating_data: RatingBase, service: RatingService = Depends()):
    return service.update_rating(rating_id, rating_data)

@router.delete("/ratings/{rating_id}", response_model=RatingSchema)
def delete_rating(rating_id: UUID, service: RatingService = Depends()):
    return service.delete_rating(rating_id)
