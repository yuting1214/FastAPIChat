from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from backend.app.crud import APICallDetailService
from backend.app.schemas import APICallDetailBase, APICallDetailCreate, APICallDetailSchema

router = APIRouter()

@router.post("/api_call_details/", response_model=APICallDetailSchema)
def create_api_call_detail(api_call_detail_data: APICallDetailCreate, service: APICallDetailService = Depends()):
    return service.create_api_call_detail(api_call_detail_data)

@router.post("/api_call_details/async", response_model=APICallDetailSchema)
async def create_api_call_detail_async(api_call_detail_data: APICallDetailCreate, service: APICallDetailService = Depends()):
    return await service.create_api_call_detail_async(api_call_detail_data)

@router.get("/api_call_details/", response_model=List[APICallDetailSchema])
def get_api_call_details(skip: int = 0, limit: int = 30, service: APICallDetailService = Depends()):
    return service.get_api_call_details(skip, limit)

@router.get("/api_call_details/{api_call_detail_id}", response_model=APICallDetailSchema)
def get_api_call_detail(api_call_detail_id: UUID, service: APICallDetailService = Depends()):
    return service.get_api_call_detail(api_call_detail_id)

@router.put("/api_call_details/{api_call_detail_id}", response_model=APICallDetailSchema)
def update_api_call_detail(api_call_detail_id: UUID, api_call_detail_data: APICallDetailBase, service: APICallDetailService = Depends()):
    return service.update_api_call_detail(api_call_detail_id, api_call_detail_data)

@router.delete("/api_call_details/{api_call_detail_id}", response_model=APICallDetailSchema)
def delete_api_call_detail(api_call_detail_id: UUID, service: APICallDetailService = Depends()):
    return service.delete_api_call_detail(api_call_detail_id)
