from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart_model import CartItem
from app.models.product_model import Product
from app.models.user_model import User
from app.schemas.cart_schema import CartItemCreate, CartItemUpdate
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    return cart_items


@router.post("/items")
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == item.product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + item.quantity

        if new_quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock available"
            )

        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)

        return {
            "message": "Cart item quantity updated",
            "cart_item": existing_item
        }

    new_cart_item = CartItem(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return {
        "message": "Product added to cart successfully",
        "cart_item": new_cart_item
    }


@router.put("/items/{cart_item_id}")
def update_cart_item(
    cart_item_id: int,
    updated_item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(Product).filter(
        Product.id == cart_item.product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if updated_item.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    cart_item.quantity = updated_item.quantity

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Cart item updated successfully",
        "cart_item": cart_item
    }


@router.delete("/items/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Cart item deleted successfully"
    }


@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "message": "Cart cleared successfully"
    }