from datetime import datetime

from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    Path,
    Query,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db

from src.services.product.schema import ProductSchema

from src.services.product.serializer import (
    ProductCreateSerializer,
    ProductUpdateSerializer
)

from src.utils.s3_helper import S3Helper

from src.utils.response import ResponseHandler


class ProductController:

    @classmethod
    async def create_product(
        cls,
        payload: ProductCreateSerializer,
        db: AsyncSession = Depends(get_db)
    ):

        image_url = await S3Helper.upload_base64_image(
            payload.product_image
        )

        payload.product_image = image_url

        new_product = await ProductSchema.create_product(
            payload,
            db
        )

        return ResponseHandler.success(
            message="Product Created Successfully",
            data={
                "id": str(new_product.id),
                "product_image": new_product.product_image,
                "title": new_product.title,
                "description": new_product.description,
                "price": new_product.price,
                "stock": new_product.stock,
                "created_at": new_product.created_at
            }
        )


    @classmethod
    async def get_all_products(
        cls,
        page: int = Query(
            default=1,
            ge=1
        ),
        limit: int = Query(
            default=5,
            ge=1,
            le=100
        ),
        search: str = Query(
            default=""
        ),
        sort: str = Query(
            default="latest"
        ),
        in_stock: bool = Query(
            default=False
        ),
        db: AsyncSession = Depends(get_db)
    ):

        products = await ProductSchema.get_all_products(
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            in_stock=in_stock,
            db=db
        )

        product_data = []

        for product in products:

            product_data.append({
                "id": str(product.id),
                "product_image": product.product_image,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "created_at": product.created_at
            })

        return ResponseHandler.success(
            message="Products Fetched Successfully",
            meta={
                "page": page,
                "limit": limit,
                "total_products": len(product_data)
            },
            data=product_data
        )


    @classmethod
    async def get_single_product(
        cls,
        product_id: UUID = Path(...),
        db: AsyncSession = Depends(get_db)
    ):

        existing_product = await ProductSchema.get_single_product(
            product_id,
            db
        )

        if not existing_product:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return ResponseHandler.success(
            message="Product Fetched Successfully",
            data={
                "id": str(existing_product.id),
                "product_image": existing_product.product_image,
                "title": existing_product.title,
                "description": existing_product.description,
                "price": existing_product.price,
                "stock": existing_product.stock,
                "created_at": existing_product.created_at
            }
        )


    @classmethod
    async def update_product(
        cls,
        payload: ProductUpdateSerializer,
        product_id: UUID = Path(...),
        db: AsyncSession = Depends(get_db)
    ):

        existing_product = await ProductSchema.get_single_product(
            product_id,
            db
        )

        if not existing_product:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # IMAGE UPDATE FLOW

        if payload.product_image:

            # DELETE OLD IMAGE FROM S3

            if existing_product.product_image:

                await S3Helper.delete_image(
                    existing_product.product_image
                )

            # UPLOAD NEW IMAGE

            image_url = await S3Helper.upload_base64_image(
                payload.product_image
            )

            payload.product_image = image_url

        payload_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in payload_data.items():

            setattr(
                existing_product,
                key,
                value
            )

        updated_product = await ProductSchema.update_product(
            existing_product,
            db
        )

        return ResponseHandler.success(
            message="Product Updated Successfully",
            data={
                "id": str(updated_product.id),
                "product_image": updated_product.product_image,
                "title": updated_product.title,
                "description": updated_product.description,
                "price": updated_product.price,
                "stock": updated_product.stock,
                "updated_at": updated_product.updated_at
            }
        )


    @classmethod
    async def delete_product(
        cls,
        product_id: UUID = Path(...),
        db: AsyncSession = Depends(get_db)
    ):

        existing_product = await ProductSchema.get_single_product(
            product_id,
            db
        )

        if not existing_product:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # DELETE IMAGE FROM S3

        if existing_product.product_image:

            await S3Helper.delete_image(
                existing_product.product_image
            )

        # SOFT DELETE DATABASE RECORD

        existing_product.is_deleted = True

        existing_product.deleted_at = datetime.utcnow()

        await ProductSchema.soft_delete_product(
            existing_product,
            db
        )

        return ResponseHandler.success(
            message="Product Deleted Successfully"
        )