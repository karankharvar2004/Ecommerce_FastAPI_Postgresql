from datetime import datetime

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

from src.services.cart.schema import CartSchema

from src.services.cart.serializer import (
    AddToCartSerializer,
    UpdateCartSerializer
)

from src.utils.response import ResponseHandler


class CartController:

    @classmethod
    async def add_to_cart(
        cls,
        payload: AddToCartSerializer,
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        existing_product = await CartSchema.get_product_by_id(
            payload.product_id,
            db
        )

        if not existing_product:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        existing_cart_item = await CartSchema.get_existing_cart_item(
            current_user.id,
            payload.product_id,
            db
        )

        if existing_cart_item:

            existing_cart_item.quantity += payload.quantity

            updated_cart_item = await CartSchema.update_cart_item(
                existing_cart_item,
                db
            )

            return ResponseHandler.success(
                message="Cart Updated Successfully",
                data={
                    "cart_id": updated_cart_item.id,
                    "product_title": updated_cart_item.product.title,
                    "quantity": updated_cart_item.quantity,
                    "price": updated_cart_item.product.price,
                    "subtotal": (
                        updated_cart_item.product.price
                        * updated_cart_item.quantity
                    )
                }
            )

        new_cart_item = await CartSchema.create_cart_item(
            user_id=current_user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            db=db
        )

        return ResponseHandler.success(
            message="Product Added To Cart",
            data={
                "cart_id": new_cart_item.id,
                "product_title": new_cart_item.product.title,
                "quantity": new_cart_item.quantity,
                "price": new_cart_item.product.price,
                "subtotal": (
                    new_cart_item.product.price
                    * new_cart_item.quantity
                )
            }
        )


    @classmethod
    async def get_cart(
        cls,
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        cart_items = await CartSchema.get_user_cart(
            current_user.id,
            db
        )

        cart_data = []

        total_amount = 0

        for item in cart_items:

            subtotal = (
                item.product.price
                * item.quantity
            )

            total_amount += subtotal

            cart_data.append({
                "cart_id": item.id,
                "product_id": item.product.id,
                "product_title": item.product.title,
                "product_image": item.product.product_image,
                "price": item.product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return ResponseHandler.success(
            message="Cart Fetched Successfully",
            meta={
                "total_amount": total_amount,
                "total_items": len(cart_data)
            },
            data=cart_data
        )


    @classmethod
    async def update_cart_quantity(
        cls,
        payload: UpdateCartSerializer,
        cart_id: UUID = Path(...),
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        existing_cart_item = await CartSchema.get_single_cart_item(
            cart_id,
            current_user.id,
            db
        )

        if not existing_cart_item:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        existing_cart_item.quantity = payload.quantity

        updated_cart_item = await CartSchema.update_cart_item(
            existing_cart_item,
            db
        )

        return ResponseHandler.success(
            message="Cart Quantity Updated Successfully",
            data={
                "cart_id": updated_cart_item.id,
                "quantity": updated_cart_item.quantity
            }
        )


    @classmethod
    async def delete_cart_item(
        cls,
        cart_id: UUID = Path(...),
        current_user: User = Depends(
            AuthDependency.get_current_user
        ),
        db: AsyncSession = Depends(get_db)
    ):

        existing_cart_item = await CartSchema.get_single_cart_item(
            cart_id,
            current_user.id,
            db
        )

        if not existing_cart_item:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        existing_cart_item.is_deleted = True

        existing_cart_item.deleted_at = datetime.utcnow()

        await CartSchema.soft_delete_cart_item(
            existing_cart_item,
            db
        )

        return ResponseHandler.success(
            message="Cart Item Deleted Successfully"
        )
