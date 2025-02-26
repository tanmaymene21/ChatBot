from typing import List, Optional
from pydantic import BaseModel, EmailStr

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    categories_offered: List[str]

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True 