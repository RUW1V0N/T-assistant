from fastapi import Depends, FastAPI
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import router as auth_router
from app.db.database import get_session

app = FastAPI()

app.include_router(auth_router)

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