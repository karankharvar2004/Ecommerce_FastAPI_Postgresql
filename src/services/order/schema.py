from uuid import UUID

from sqlalchemy import select

from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.order_model import Order


class OrderSchema:

    @classmethod
    async def get_user_orders(
        cls,
        user_id: UUID,
        db: AsyncSession
    ):

        query = (
            select(Order)
            .options(
                selectinload(Order.product)
            )
            .where(
                Order.user_id == user_id,
                Order.is_deleted == False
            )
        )

        result = await db.execute(query)

        return result.scalars().all()


    @classmethod
    async def get_single_order(
        cls,
        order_id: UUID,
        user_id: UUID,
        db: AsyncSession
    ):

        query = (
            select(Order)
            .options(
                selectinload(Order.product)
            )
            .where(
                Order.id == order_id,
                Order.user_id == user_id,
                Order.is_deleted == False
            )
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()
