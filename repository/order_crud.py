
from http.client import HTTPException
from sqlalchemy.orm import Session
from model.product_model import  Product,ProductImage
from model.order_mdel import Order, OrderItem

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


def get_all_orders_by_id(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()




def get_order_details(db: Session, user_id: int):
        """
        Get all order details including products, quantities, and images for a specific user.
        """
        orders = db.query(Order).filter(Order.user_id == user_id).all()

        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user")

        order_details = []
        for order in orders:
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            item_details = []
            for item in items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                images = db.query(ProductImage).filter(ProductImage.product_id == product.id).all()
                image_urls = [image.image_url for image in images]  # Get the image URLs

                item_details.append({
                    "product_name": product.name,
                    "description": product.description,
                    "quantity": item.quantity,
                    "price_per_unit": product.price,
                    "total_price_for_item": product.price * item.quantity,
                    "images": image_urls  # Add image URLs to the response
                })
            order_details.append({
                "order_id": order.id,
                "total_order_price": order.total_price,
                "items": item_details
            })
        return order_details