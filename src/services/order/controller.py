from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    Path,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db

from src.database.dependencies import AuthDependency

from src.database.models.user_model import User

from src.services.order.schema import OrderSchema

from src.utils.response import ResponseHandler


class OrderController:

    @classmethod
    async def get_orders(
        cls,
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        orders = await OrderSchema.get_user_orders(
            current_user.id,
            db
        )

        order_data = []

        total_spent = 0

        for order in orders:

            total_spent += order.subtotal

            order_data.append({
                "order_id": order.id,
                "product_id": order.product.id,
                "product_title": order.product.title,
                "product_image": order.product.product_image,
                "quantity": order.quantity,
                "price": order.price,
                "subtotal": order.subtotal,
                "payment_status": order.payment_status,
                "ordered_at": order.created_at
            })

        return ResponseHandler.success(
            message="Orders Fetched Successfully",
            meta={
                "total_orders": len(order_data),
                "total_spent": total_spent
            },
            data=order_data
        )


    @classmethod
    async def get_single_order(
        cls,
        order_id: UUID = Path(...),
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        order = await OrderSchema.get_single_order(
            order_id,
            current_user.id,
            db
        )

        if not order:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        return ResponseHandler.success(
            message="Order Fetched Successfully",
            data={
                "order_id": order.id,
                "product_id": order.product.id,
                "product_title": order.product.title,
                "product_image": order.product.product_image,
                "quantity": order.quantity,
                "price": order.price,
                "subtotal": order.subtotal,
                "payment_status": order.payment_status,
                "ordered_at": order.created_at
            }
        )
