from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from src.database.db_config import get_db

from src.database.jwt_handler import decode_access_token

from src.database.models.user_model import User


security = HTTPBearer()


class AuthDependency:

    @classmethod
    async def get_current_user(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ):

        token = credentials.credentials

        payload = decode_access_token(token)

        if not payload:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        try:

            user_id = UUID(payload.get("user_id"))

        except (TypeError, ValueError):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        query = select(User).where(
            User.id == user_id,
            User.is_deleted == False
        )

        result = await db.execute(query)

        existing_user = result.scalar_one_or_none()

        if not existing_user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return existing_user
