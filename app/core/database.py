from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()


# Synchronous database URL for Alembic
SYNC_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

Base = declarative_base()
# Asynchronous engine

# Synchronous engine for Alembic
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Asynchronous session
SessionLocal = sessionmaker(bind=sync_engine)

# Dependency
def get_db():
    with SessionLocal() as session:
        yield session

