from pydantic import BaseModel
from typing import Optional


class House(BaseModel):
    name: str
    address: str = None
    price: float
    sqft: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Seinfeld Apartment",
                "address": "Apartment 5A, 129 W. 81st St., New York, N.Y.",
                "price": 1000,
                "sqft": 300,
            }
        }


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
