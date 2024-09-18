from pydantic import BaseModel
from typing import List, Optional



class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(BaseModel):
    id: int  
    order_id: int  
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    total_price: float
    items: List[OrderItem]

    class Config:
        orm_mode = True
