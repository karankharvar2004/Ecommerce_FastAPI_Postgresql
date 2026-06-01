import uuid

from sqlalchemy import (
    Column,
    Float,
    String,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from src.database.db_config import Base

from src.database.models.base_model import BaseModel


class Payment(Base, BaseModel):

    __tablename__ = "payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    payment_status = Column(
        String,
        default="success"
    )

    transaction_id = Column(
        String,
        nullable=False
    )


    user = relationship(
        "User"
    )
