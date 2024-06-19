from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import LLM

def create_llm_crud(db: Session, llm_data: dict):
    # Check if the model already exists
    existing_model = db.query(LLM).filter_by(llm_model_name=llm_data["llm_model_name"], llm_vendor=llm_data["llm_vendor"]).first()
    if existing_model:
        return existing_model
    
    # If not, insert the new model
    db_llm = LLM(**llm_data)
    db.add(db_llm)
    db.commit()
    db.refresh(db_llm)
    return db_llm

async def create_llm_crud_async(db: AsyncSession, llm_data: dict):
    # Check if the model already exists
    stmt = select(LLM).filter_by(llm_model_name=llm_data["llm_model_name"], llm_vendor=llm_data["llm_vendor"])
    result = await db.execute(stmt)
    existing_model = result.scalars().first()
    if existing_model:
        return existing_model

    # If not, insert the new model asynchronously
    db_llm = LLM(**llm_data)
    db.add(db_llm)
    await db.commit()  # Use await for asynchronous commit operation
    await db.refresh(db_llm)  # Use await for asynchronous refresh operation
    return db_llm

# Define asynchronous helper functions for async DB operations
async def get_llm_from_db(db: Session, endpoint: str):
    return await db.query(LLM).filter(LLM.api_endpoint == endpoint).first()