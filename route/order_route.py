

from typing import List
from fastapi import  Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import  OAuth2PasswordBearer
from repository import order_crud
from schema import order_schema
from security.user_security import verify_token


order_Router = APIRouter(prefix="/order")


@order_Router.post("/orders/", response_model=order_schema.Order, tags=["order"])
def create_order(
    order: order_schema.OrderCreate,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    try:
        return order_crud.create_order(db=db, user_id=user_id, items=order.items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@order_Router.get("/orders/", response_model=List[order_schema.Order], tags=["order"])
def get_orders_by_user(
    user_id: str = Depends(verify_token),  # Ensure the token is verified and user_id is extracted
    db: Session = Depends(get_db)
):
    try:
        orders = order_crud.get_all_orders_by_id(db, user_id)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Get an order by ID
@order_Router.get("/order/{order_id}", response_model=order_schema.Order, tags=["order"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order_by_id(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_Router.get("/users/{user_id}/order-details/")
def get_user_order_details(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        orders = order_crud.get_order_details(db, user_id)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


