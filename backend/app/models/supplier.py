from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    categories_offered = Column(JSON)  
    
    products = relationship("Product", back_populates="supplier") 