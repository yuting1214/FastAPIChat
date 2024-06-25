from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from backend.app.core.init_settings import global_settings as settings

# Base class for the database models
Base = declarative_base()

# Synchronous engine and session
sync_engine = create_engine(settings.DB_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Asynchronous engine and session
async_engine = create_async_engine(settings.ASYNC_DB_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

def init_db():
    Base.metadata.create_all(bind=sync_engine)