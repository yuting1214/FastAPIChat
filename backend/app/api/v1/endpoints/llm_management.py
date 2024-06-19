from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.dependencies.database import get_sync_db
from backend.app.models import LLM
from backend.app.schemas import (
    LLMCreate,
    LLMUpdate,
    LLMSchema
)

router = APIRouter()

@router.post("/llms/", response_model=LLMSchema)
def create_llm(llm_data: LLMCreate, db: Session = Depends(get_sync_db)):
    db_llm = LLM(**llm_data.model_dump())
    db.add(db_llm)
    db.commit()
    db.refresh(db_llm)
    return db_llm

@router.get("/llms/id/{llm_id}", response_model=LLMSchema)
def read_llm(llm_id: UUID, db: Session = Depends(get_sync_db)):
    db_llm = db.query(LLM).filter(LLM.id == llm_id).first()
    if db_llm is None:
        raise HTTPException(status_code=404, detail="LLM not found")
    return db_llm

@router.get("/llms/", response_model=List[LLMSchema])
def read_llms(skip: int = 0, limit: int = 10, db: Session = Depends(get_sync_db)):
    return db.query(LLM).offset(skip).limit(limit).all()

@router.get("/llms/type/{llm_type}", response_model=List[LLMSchema])
def read_llms_by_type(llm_type: str, db: Session = Depends(get_sync_db)):
    db_llms = db.query(LLM).filter(LLM.llm_type == llm_type).all()
    if not db_llms:
        raise HTTPException(status_code=404, detail=f"No LLMs found for type '{llm_type}'")
    return db_llms

@router.put("/llms/id/{llm_id}", response_model=LLMSchema)
def update_llm(llm_id: UUID, llm_data: LLMUpdate, db: Session = Depends(get_sync_db)):
    db_llm = db.query(LLM).filter(LLM.id == llm_id).first()
    if db_llm is None:
        raise HTTPException(status_code=404, detail="Message not found")
    for key, value in llm_data.model_dump().items():
        setattr(db_llm, key, value)
    db.commit()
    db.refresh(db_llm)
    return db_llm

@router.delete("/llms/id/{llm_id}", response_model=LLMSchema)
def delete_llm(llm_id: UUID, db: Session = Depends(get_sync_db)):
    db_llm = db.query(LLM).filter(LLM.id == llm_id).first()
    if db_llm is None:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(db_llm)
    db.commit()
    return db_llm
