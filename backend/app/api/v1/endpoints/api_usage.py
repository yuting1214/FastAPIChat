from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from backend.app.crud import APIUsageService
from backend.app.schemas import APIUsageBase, APIUsageCreate, APIUsageSchema

router = APIRouter()

@router.post("/api_usages/", response_model=APIUsageSchema)
def create_api_usage(api_usage_data: APIUsageCreate, service: APIUsageService = Depends()):
    return service.create_api_usage(api_usage_data)

@router.post("/api_usages/async", response_model=APIUsageSchema)
async def create_api_usage_async(api_usage_data: APIUsageCreate, service: APIUsageService = Depends()):
    return await service.create_api_usage_async(api_usage_data)

@router.get("/api_usages/", response_model=List[APIUsageSchema])
def get_api_usages(skip: int = 0, limit: int = 30, service: APIUsageService = Depends()):
    return service.get_api_usages(skip, limit)

@router.get("/api_usages/{api_usage_id}", response_model=APIUsageSchema)
def get_api_usage(api_usage_id: UUID, service: APIUsageService = Depends()):
    return service.get_api_usage(api_usage_id)

@router.put("/api_usages/{api_usage_id}", response_model=APIUsageSchema)
def update_api_usage(api_usage_id: UUID, api_usage_data: APIUsageBase, service: APIUsageService = Depends()):
    return service.update_api_usage(api_usage_id, api_usage_data)

@router.delete("/api_usages/{api_usage_id}", response_model=APIUsageSchema)
def delete_api_usage(api_usage_id: UUID, service: APIUsageService = Depends()):
    return service.delete_api_usage(api_usage_id)
