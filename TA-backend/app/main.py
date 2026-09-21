from fastapi import Depends, FastAPI
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Training Assistant API"}


@app.get("/health/db")
async def database_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))

    return {
        "database": "ok",
        "result": result.scalar(),
    }