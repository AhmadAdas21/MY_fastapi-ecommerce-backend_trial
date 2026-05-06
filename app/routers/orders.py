from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.models.cart_model import CartItem
from app.models.product_model import Product
from app.models.order_model import Order, OrderItem
from app.schemas.order_schema import OrderStatusUpdate
from app.utils.dependencies import get_current_user, get_current_admin

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0

    for item in cart_items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.is_active == True
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {item.product_id} not found"
            )

        if item.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.name}"
            )

        total_price += product.price * item.quantity

    new_order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        subtotal = product.price * item.quantity

        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        )

        product.stock_quantity -= item.quantity

        db.add(new_order_item)
        order_items.append(new_order_item)

    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "message": "Order created successfully",
        "order": {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "total_price": new_order.total_price,
            "status": new_order.status
        },
        "items_count": len(order_items)
    }


@router.get("/my-orders")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    return orders


@router.get("/{order_id}")
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to view this order")

    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    return {
        "order": order,
        "items": order_items
    }


@router.get("/admin/all")
def get_all_orders(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    orders = db.query(Order).all()
    return orders


@router.put("/admin/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "order": order
    }