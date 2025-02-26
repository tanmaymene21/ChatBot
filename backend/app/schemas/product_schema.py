from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    category: str
    description: str
    supplier_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True 