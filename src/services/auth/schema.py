from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user_model import User


class AuthSchema:

    @classmethod
    async def get_user_by_email(
        cls,
        email: str,
        db: AsyncSession
    ):

        query = select(User).where(
            User.email == email,
            User.is_deleted == False
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @classmethod
    async def create_user(
        cls,
        username: str,
        email: str,
        hashed_password: str,
        db: AsyncSession
    ):

        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        db.add(new_user)

        await db.commit()

        await db.refresh(new_user)

        return new_user