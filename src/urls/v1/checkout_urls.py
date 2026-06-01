from fastapi import APIRouter

from src.services.checkout.controller import (
    CheckoutController
)


router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"]
)


router.post("/")(
    CheckoutController.checkout
)