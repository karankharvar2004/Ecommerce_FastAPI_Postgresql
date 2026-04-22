# app/routes/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ecommerce.database import get_db
from ecommerce.models import Product, Cart, CartItem, Order
from ecommerce.schemas import (
    AddToCartRequest,
    ProductCreate,
    ProductResponse,
    RemoveFromCartRequest,
    CheckoutRequest
)

router = APIRouter()


# ---------------- PRODUCTS ----------------

@router.get("/products/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.created_at.desc()).all()


@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.patch("/products/{product_id}", response_model=ProductResponse)
def partial_update_product(product_id: int, data: dict, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Only update provided fields
    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Deleted successfully"}


# ---------------- CART ----------------

@router.post("/cart/add/")
def add_to_cart(data: AddToCartRequest, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create or get cart
    if data.cart_id:
        cart = db.query(Cart).filter(Cart.id == data.cart_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
    else:
        cart = Cart()
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check if item exists
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    if cart_item:
        cart_item.quantity += data.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(cart_item)

    db.commit()

    return {
        "message": "Added to cart",
        "cart_id": cart.id,
        "quantity": cart_item.quantity
    }


@router.post("/cart/remove/")
def remove_from_cart(data: RemoveFromCartRequest, db: Session = Depends(get_db)):

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == data.cart_id,
        CartItem.product_id == data.product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.delete(cart_item)

    db.commit()

    return {"message": "Updated cart"}


@router.get("/cart/{cart_id}")
def get_cart(cart_id: int, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    total = 0
    response_items = []

    for item in items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        response_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": float(item.product.price),
            "subtotal": float(subtotal)
        })

    return {
        "cart_id": cart.id,
        "items": response_items,
        "total": float(total)
    }


# ---------------- CHECKOUT ----------------

@router.post("/checkout/")
def checkout(data: CheckoutRequest, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.id == data.cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = db.query(CartItem).filter(CartItem.cart_id == data.cart_id).all()

    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.product.price * item.quantity for item in items)

    order = Order(
        cart_id=cart.id,
        total_amount=total,
        is_paid=True
    )

    db.add(order)

    # Clear cart after checkout
    for item in items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return {
        "order_id": order.id,
        "total_amount": float(order.total_amount),
        "status": "Paid"
    }