from uuid import UUID

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.cart_model import Cart

from src.database.models.product_model import Product

from sqlalchemy.orm import selectinload


class CartSchema:

    @classmethod
    async def get_product_by_id(
        cls,
        product_id: UUID,
        db: AsyncSession
    ):

        query = select(Product).where(
            Product.id == product_id,
            Product.is_deleted == False
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @classmethod
    async def get_existing_cart_item(
        cls,
        user_id: UUID,
        product_id: UUID,
        db: AsyncSession
    ):

        query = select(Cart).where(
            Cart.user_id == user_id,
            Cart.product_id == product_id,
            Cart.is_deleted == False
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @classmethod
    async def create_cart_item(
        cls,
        user_id: UUID,
        product_id: UUID,
        quantity: int,
        db: AsyncSession
    ):

        new_cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(new_cart_item)

        await db.commit()

        await db.refresh(new_cart_item)

        return new_cart_item


    @classmethod
    async def update_cart_item(
        cls,
        existing_cart_item,
        db: AsyncSession
    ):

        await db.commit()

        await db.refresh(existing_cart_item)

        return existing_cart_item


    @classmethod
    async def get_user_cart(
        cls,
        user_id: UUID,
        db: AsyncSession
    ):

        query = (select(Cart).options(selectinload(Cart.product))
        .where(
            Cart.user_id == user_id,
            Cart.is_deleted == False
        )
    )

        result = await db.execute(query)

        return result.scalars().all()


    @classmethod
    async def get_single_cart_item(
        cls,
        cart_id: UUID,
        user_id: UUID,
        db: AsyncSession
    ):

        query = (
        select(Cart)
        .options(
            selectinload(Cart.product)
        )
        .where(
            Cart.id == cart_id,
            Cart.user_id == user_id,
            Cart.is_deleted == False
        )
    )

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @classmethod
    async def soft_delete_cart_item(
        cls,
        existing_cart_item,
        db: AsyncSession
    ):

        await db.commit()

        return True
