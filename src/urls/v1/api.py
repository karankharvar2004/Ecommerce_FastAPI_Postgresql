from fastapi import APIRouter

from src.urls.v1.auth_urls import (
    router as auth_router
)

from src.urls.v1.product_urls import (
    router as product_router
)

from src.urls.v1.cart_urls import (
    router as cart_router
)

from src.urls.v1.checkout_urls import (
    router as checkout_router
)

from src.urls.v1.order_urls import (
    router as order_router
)

router = APIRouter()


router.include_router(auth_router)

router.include_router(product_router)

router.include_router(cart_router)

router.include_router(checkout_router)

router.include_router(order_router)