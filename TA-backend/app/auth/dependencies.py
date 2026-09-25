from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_access_token
from app.db.database import get_session
from app.models.user import User

http_bearer = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        session: AsyncSession = Depends(get_session),
) -> User:
    token = credentials.credentials
    
    user_id = decode_access_token(token)

    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user