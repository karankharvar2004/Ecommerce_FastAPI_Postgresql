from uuid import UUID

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.product_model import Product

from sqlalchemy import or_

from sqlalchemy import asc, desc


class ProductSchema:

    @classmethod
    async def create_product(
        cls,
        payload,
        db: AsyncSession
    ):

        new_product = Product(
            product_image=payload.product_image,
            title=payload.title,
            description=payload.description,
            price=payload.price,
            stock=payload.stock
        )

        db.add(new_product)

        await db.commit()

        await db.refresh(new_product)

        return new_product


    @classmethod
    async def get_all_products(
        cls,
        page: int,
        limit: int,
        search: str,
        sort: str,
        in_stock: bool,
        db: AsyncSession
    ):

        query = select(Product).where(
            Product.is_deleted == False
        )

        # SEARCH

        if search:

            query = query.where(
                or_(
                    Product.title.ilike(
                        f"%{search}%"
                    ),
                    Product.description.ilike(
                        f"%{search}%"
                    )
                )
            )

        # STOCK FILTER

        if in_stock:

            query = query.where(
                Product.stock > 0
            )

        # SORTING

        if sort == "price_asc":

            query = query.order_by(
                asc(Product.price)
            )

        elif sort == "price_desc":

            query = query.order_by(
                desc(Product.price)
            )

        elif sort == "latest":

            query = query.order_by(
                desc(Product.created_at)
            )

        # PAGINATION

        offset = (page - 1) * limit

        query = query.offset(offset).limit(limit)

        result = await db.execute(query)

        return result.scalars().all()


    @classmethod
    async def get_single_product(
        cls,
        product_id: UUID,
        db: AsyncSession
    ):

        query = select(Product).where(
            Product.id == product_id,
            Product.is_deleted == False
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @classmethod
    async def update_product(
        cls,
        existing_product,
        db: AsyncSession
    ):

        await db.commit()

        await db.refresh(existing_product)

        return existing_product


    @classmethod
    async def soft_delete_product(
        cls,
        existing_product,
        db: AsyncSession
    ):

        await db.commit()

        return True
