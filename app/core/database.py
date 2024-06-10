from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# Asynchronous database URL
ASYNC_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

# Synchronous database URL for Alembic
SYNC_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

Base = declarative_base()
# Asynchronous engine
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Synchronous engine for Alembic
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Asynchronous session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

