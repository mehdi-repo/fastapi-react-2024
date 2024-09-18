from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer
from database.connection import Base
from sqlalchemy.orm import  relationship


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)  
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")  



class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    order = relationship("Order", back_populates="items")  
    product = relationship("Product", back_populates="order_items")  

