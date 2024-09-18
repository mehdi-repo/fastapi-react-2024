from pydantic import BaseModel
from typing import List, Optional

class ProductImageBase(BaseModel):
    image_url: str

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int
    product_id: int
    
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    image_urls: List[str]

class Product(ProductBase):
    id: int
    image_urls: List[str]

    class Config:
        orm_mode = True




