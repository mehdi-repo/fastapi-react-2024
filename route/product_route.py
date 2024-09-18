

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile,APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import  OAuth2PasswordBearer
from model import user_model
from repository import product_crud
from schema import product_schema
from security.user_security import  authenticate_user, get_current_user, verify_token


product_Router = APIRouter(prefix="/product")


# Create a product
@product_Router.post("/products/", response_model=product_schema.Product,tags=["product"])
async def create_product(
    name: str,
    description: str,
    price: float,
    files: List[UploadFile] = File(...), 
    current_user: user_model.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Check if the current user is an admin
    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to perform this action."
        )
    
    # Create product and save images
    created_product = product_crud.create_product(
        db=db,
        name=name,
        description=description,
        price=price,
        image_files=files
    )
    
    return created_product



# Get all products
@product_Router.get("/products/", response_model=List[product_schema.Product], tags=["product"])
def read_products(db: Session = Depends(get_db)):
    products = product_crud.get_products(db=db)
    return products


# Get product by ID
@product_Router.get("/products/{product_id}", response_model=product_schema.Product, tags=["product"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product




