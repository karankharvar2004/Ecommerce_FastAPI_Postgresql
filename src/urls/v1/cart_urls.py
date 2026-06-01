from fastapi import APIRouter

from src.services.cart.controller import (
    CartController
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


router.post("/")(
    CartController.add_to_cart
)

router.get("/")(
    CartController.get_cart
)

router.patch("/{cart_id}")(
    CartController.update_cart_quantity
)

router.delete("/{cart_id}")(
    CartController.delete_cart_item
)