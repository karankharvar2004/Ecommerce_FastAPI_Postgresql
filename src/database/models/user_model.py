import uuid

from sqlalchemy import (
    Column,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from src.database.db_config import Base

from src.database.models.base_model import BaseModel


class User(Base, BaseModel):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    username = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )
