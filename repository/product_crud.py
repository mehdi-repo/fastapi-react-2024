import os
from typing import Dict, List
from sqlalchemy.orm import Session
from model.product_model import  Product, ProductImage
from model.order_mdel import Order, OrderItem




BASE_URL = "http://127.0.0.1:8000/"


def create_product(db: Session, name: str, description: str, price: float, image_files: List[str]):
    # Create product instance
    product = Product(name=name, description=description, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Create a directory for the product using its ID
    product_dir = os.path.join("static/product_images", str(product.id))
    os.makedirs(product_dir, exist_ok=True)
    
    # Save product images
    image_urls = []
    for file in image_files:
        file_path = os.path.join(product_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        image_urls.append(f"/static/product_images/{product.id}/{file.filename}")
        
        # Save image metadata to the database
        image = ProductImage(product_id=product.id, image_url=f"/static/product_images/{product.id}/{file.filename}")
        db.add(image)
    
    db.commit()
    
    # Include image_urls in the returned product object
    product.image_urls = image_urls
    return product



def get_products(db: Session):
    products = db.query(Product).all()
    for product in products:
        product.image_urls = [os.path.join(BASE_URL, image.image_url) for image in product.images]
    return products



def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.image_urls = [image.image_url for image in product.images]  # Attach image URLs
    return product




def create_order(db: Session, user_id: int, items: list):
    total_price = 0
    order_items = []

    # Calculate total price and prepare order items
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product with id {item.product_id} not found.")
        
        total_price += product.price * item.quantity
        order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
        order_items.append(order_item)

    # Create and commit order
    order = Order(user_id=user_id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)  # Populate order ID after committing
    
    # Commit each order item
    for order_item in order_items:
        order_item.order_id = order.id  # Set order_id for each item
        db.add(order_item)
    db.commit()

    # Refresh to get IDs of order items
    db.refresh(order)
    for order_item in order.items:
        db.refresh(order_item)
    
    return order


def get_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()




