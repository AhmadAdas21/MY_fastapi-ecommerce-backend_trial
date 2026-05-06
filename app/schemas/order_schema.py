from pydantic import BaseModel
from typing import Literal


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True








class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "paid", "shipped", "delivered", "cancelled"]