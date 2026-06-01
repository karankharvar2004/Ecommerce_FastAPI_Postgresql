from typing import Annotated

from pydantic import (
    BaseModel,
    StringConstraints,
    Field
)

from decimal import Decimal


class ProductCreateSerializer(BaseModel):

    title: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200
        )
    ]

    description: Annotated[
        str,
        StringConstraints(
            min_length=10
        )
    ]

    price: Decimal = Field(
        gt=0
    )

    stock: int = Field(
        ge=0
    )

    product_image: Annotated[
    str,
    StringConstraints(
        min_length=20
    )
]


class ProductUpdateSerializer(BaseModel):

    title: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=200
        )
    ] | None = None

    description: Annotated[
        str,
        StringConstraints(
            min_length=10
        )
    ] | None = None

    price: Decimal | None = Field(
        default=None,
        gt=0
    )

    stock: int | None = Field(
        default=None,
        ge=0
    )

    product_image: Annotated[
        str,
        StringConstraints(
            min_length=20
        )
    ] | None = None