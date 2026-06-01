from uuid import UUID

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.cart_model import Cart

from src.database.models.order_model import Order

from src.database.models.payment_model import Payment

from src.database.models.product_model import Product

from sqlalchemy.orm import selectinload

class CheckoutSchema:

    @classmethod
    async def get_user_cart(
        cls,
        user_id: UUID,
        db: AsyncSession
    ):

        query = (
        select(Cart)
        .options(
            selectinload(Cart.product)
        )
        .where(
            Cart.user_id == user_id,
            Cart.is_deleted == False
        )
    )

        result = await db.execute(query)

        return result.scalars().all()


    @classmethod
    async def create_payment(
        cls,
        user_id: UUID,
        total_amount: float,
        transaction_id: str,
        db: AsyncSession
    ):

        payment = Payment(
            user_id=user_id,
            total_amount=total_amount,
            payment_status="success",
            transaction_id=transaction_id
        )

        db.add(payment)

        await db.commit()

        await db.refresh(payment)

        return payment


    @classmethod
    async def create_order(
        cls,
        user_id: UUID,
        product_id: UUID,
        quantity: int,
        price: float,
        subtotal: float,
        db: AsyncSession
    ):

        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
            subtotal=subtotal,
            payment_status="success"
        )

        db.add(order)

        await db.commit()

        await db.refresh(order)

        return order


    @classmethod
    async def update_product_stock(
        cls,
        product,
        db: AsyncSession
    ):

        await db.commit()

        await db.refresh(product)

        return product


    @classmethod
    async def clear_cart_item(
        cls,
        cart_item,
        db: AsyncSession
    ):

        await db.commit()

        return True
