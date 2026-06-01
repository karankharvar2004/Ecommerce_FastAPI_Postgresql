import uuid

from datetime import datetime

from fastapi import (
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db

from src.database.dependencies import AuthDependency

from src.database.models.user_model import User

from src.services.checkout.schema import CheckoutSchema

from src.utils.response import ResponseHandler


class CheckoutController:

    @classmethod
    async def checkout(
        cls,
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        cart_items = await CheckoutSchema.get_user_cart(
            current_user.id,
            db
        )

        if not cart_items:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        total_amount = 0

        order_summary = []

        for item in cart_items:

            if item.quantity > item.product.stock:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient stock for "
                        f"{item.product.title}"
                    )
                )

            subtotal = (
                item.product.price
                * item.quantity
            )

            total_amount += subtotal

        transaction_id = (
            f"TXN_{uuid.uuid4().hex[:10].upper()}"
        )

        payment = await CheckoutSchema.create_payment(
            user_id=current_user.id,
            total_amount=total_amount,
            transaction_id=transaction_id,
            db=db
        )

        for item in cart_items:

            subtotal = (
                item.product.price
                * item.quantity
            )

            order = await CheckoutSchema.create_order(
                user_id=current_user.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=subtotal,
                db=db
            )

            item.product.stock -= item.quantity

            await CheckoutSchema.update_product_stock(
                item.product,
                db
            )

            item.is_deleted = True

            item.deleted_at = datetime.utcnow()

            await CheckoutSchema.clear_cart_item(
                item,
                db
            )

            order_summary.append({
                "order_id": order.id,
                "product_title": item.product.title,
                "quantity": item.quantity,
                "price": item.product.price,
                "subtotal": subtotal
            })

        return ResponseHandler.success(
            message="Checkout Completed Successfully",
            data={
                "payment": {
                    "payment_id": payment.id,
                    "transaction_id": payment.transaction_id,
                    "total_amount": payment.total_amount,
                    "payment_status": payment.payment_status
                },
                "orders": order_summary
            }
        )