from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token


from app.db.database import get_session
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register",response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
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

    access_token = create_access_token(user.id)
    
    return{
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session), 
):
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }