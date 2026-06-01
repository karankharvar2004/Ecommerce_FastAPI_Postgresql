from fastapi import (
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db

from src.database.dependencies import AuthDependency

from src.database.models.user_model import User

from src.database.jwt_handler import (
    create_access_token,
    create_refresh_token
)

from src.utils.helpers import PasswordHelper

from src.utils.response import ResponseHandler

from src.services.auth.schema import AuthSchema

from src.services.auth.serializer import (
    RegisterSerializer,
    LoginSerializer
)


class AuthController:

    @classmethod
    async def register(
        cls,
        payload: RegisterSerializer,
        db: AsyncSession = Depends(get_db)
    ):

        existing_user = await AuthSchema.get_user_by_email(
            payload.email,
            db
        )

        if existing_user:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        hashed_password = PasswordHelper.hash_password(
            payload.password
        )

        new_user = await AuthSchema.create_user(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed_password,
            db=db
        )

        return ResponseHandler.success(
            message="User Registered Successfully",
            data={
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at
            }
        )


    @classmethod
    async def login(
        cls,
        payload: LoginSerializer,
        db: AsyncSession = Depends(get_db)
    ):

        existing_user = await AuthSchema.get_user_by_email(
            payload.email,
            db
        )

        if not existing_user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid email or password"
            )

        is_password_valid = PasswordHelper.verify_password(
            payload.password,
            existing_user.hashed_password
        )

        if not is_password_valid:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password"
            )

        token_data = {
            "user_id": str(existing_user.id),
            "email": existing_user.email
        }

        access_token = create_access_token(
            token_data
        )

        refresh_token = create_refresh_token(
            token_data
        )

        return ResponseHandler.success(
            message="Login Successful",
            data={
                "user": {
                    "id": existing_user.id,
                    "username": existing_user.username,
                    "email": existing_user.email
                },
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }
        )


    @classmethod
    async def me(
        cls,
        current_user: User = Depends(
            AuthDependency.get_current_user
        )
    ):

        return ResponseHandler.success(
            message="Current User Fetched Successfully",
            data={
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email
            }
        )
