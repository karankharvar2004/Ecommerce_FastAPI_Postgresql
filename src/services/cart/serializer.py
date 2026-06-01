from uuid import UUID

from pydantic import (
    BaseModel,
    Field
)


class AddToCartSerializer(BaseModel):

    product_id: UUID

    quantity: int = Field(
        ge=1
    )


class UpdateCartSerializer(BaseModel):

    quantity: int = Field(
        ge=1
    )
