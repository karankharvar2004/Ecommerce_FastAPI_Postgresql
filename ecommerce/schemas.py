# app/schemas/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# -------------------- PRODUCT --------------------

class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------- CART ITEM --------------------

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    subtotal: Decimal

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------- CART --------------------

class CartResponse(BaseModel):
    id: int
    created_at: datetime
    items: List[CartItemResponse]
    total: Decimal

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------- ORDER --------------------

class OrderResponse(BaseModel):
    id: int
    total_amount: Decimal
    is_paid: bool
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------- REQUEST SCHEMAS --------------------

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    cart_id: Optional[int] = None


class RemoveFromCartRequest(BaseModel):
    product_id: int
    cart_id: int


class CheckoutRequest(BaseModel):
    cart_id: int