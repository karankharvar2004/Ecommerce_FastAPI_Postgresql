from fastapi import (
    APIRouter,
    Depends
)

from src.services.product.controller import (
    ProductController
)

from src.database.dependencies import (
    AuthDependency
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


router.post(
    "/",
    dependencies=[
        Depends(
            AuthDependency.get_current_user
        )
    ]
)(
    ProductController.create_product
)


router.get("/")(
    ProductController.get_all_products
)


router.get("/{product_id}")(
    ProductController.get_single_product
)


router.patch(
    "/{product_id}",
    dependencies=[
        Depends(
            AuthDependency.get_current_user
        )
    ]
)(
    ProductController.update_product
)


router.delete(
    "/{product_id}",
    dependencies=[
        Depends(
            AuthDependency.get_current_user
        )
    ]
)(
    ProductController.delete_product
)