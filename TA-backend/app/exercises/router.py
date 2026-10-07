from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.database import get_session
from app.models.exercise import Exercise
from app.models.user import User
from app.exercises.schemas import ExerciseRead

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
)

@router.get("/", response_model=list[ExerciseRead])
async def get_exercises(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Exercise)
    )

    exercises = result.scalars().all()

    return exercises
