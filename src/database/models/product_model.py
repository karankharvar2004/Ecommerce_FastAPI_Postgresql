import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text
)

from sqlalchemy.dialects.postgresql import UUID

from src.database.db_config import Base

from src.database.models.base_model import BaseModel


class Product(Base, BaseModel):

    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    product_image = Column(
        Text,
        nullable=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    stock = Column(
        Integer,
        default=0
    )
