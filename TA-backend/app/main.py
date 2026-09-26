from fastapi import Depends, FastAPI
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import router as auth_router
from app.db.database import get_session
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.auth.schemas.user import UserResponse

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

@app.get("/users/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
