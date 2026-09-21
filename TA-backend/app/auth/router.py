from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas.user import UserRegister
from app.auth.security import hash_password
from app.db.database import get_session
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session),
):
    result= await session.execute(
        select(User).where(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    user= User(
        username=user_data.username,
        email= user_data.email,
        hashed_password=hash_password(user_data.password), 
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }
