from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    StringConstraints
)


class RegisterSerializer(BaseModel):

    username: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=50
        )
    ]

    email: EmailStr

    password: Annotated[
        str,
        StringConstraints(
            min_length=6,
            max_length=100
        )
    ]


class LoginSerializer(BaseModel):

    email: EmailStr

    password: Annotated[
        str,
        StringConstraints(
            min_length=6,
            max_length=100
        )
    ]