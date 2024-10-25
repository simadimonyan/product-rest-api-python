from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Float, Integer, String
from hashlib import sha256
from pydantic import BaseModel

# base orm model
class Base(DeclarativeBase): 
    pass

# orm model
class Product(Base):
    __tablename__ = 'products'  
    
    id = Column(String(256), primary_key=True)
    category = Column(String(256))
    name = Column(String(256))
    amount = Column(Integer)
    cost = Column(Float)
    currency = Column(String(256))


    def __init__(self, category, name, amount, cost, currency):
        data = f"{category} {name}"
        # id hash generating
        self.id = str(sha256(data.encode("utf-8")).hexdigest()) 
        self.category = category
        self.name = name
        self.amount = amount
        self.cost = cost
        self.currency = currency

    # serialization to json
    def toJSON(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "cost": self.cost,
            "amount": self.amount,
            "currency": self.currency
        }
    
    # regenerating id
    def refresh(self):
        data = f"{self.category} {self.name}"
        # id hash generating
        self.id = str(sha256(data.encode("utf-8")).hexdigest()) 

# meta class for pydantic json response
class ProductResponse(BaseModel):
    category: str
    name: str
    amount: int
    cost: float 
    currency: str
