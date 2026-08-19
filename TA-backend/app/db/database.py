import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_async_engine(
    DATABASE_URL,
    echo= True,
)

async_session = async_sessionmaker(
    engine,
    class_= AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with async_session() as session:
        yield session