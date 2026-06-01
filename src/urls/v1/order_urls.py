from fastapi import APIRouter

from src.services.order.controller import (
    OrderController
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


router.get("/")(
    OrderController.get_orders
)

router.get("/{order_id}")(
    OrderController.get_single_order
)