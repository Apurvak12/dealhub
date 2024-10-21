from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class PriceHistory(BaseModel):
    price: float
    date: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    email: EmailStr

class Product(BaseModel):
    url: str = Field(..., unique=True)
    currency: str
    image: str
    title: str
    currentPrice: float
    originalPrice: float
    priceHistory: List[PriceHistory]
    lowestPrice: Optional[float] = None
    highestPrice: Optional[float] = None
    averagePrice: Optional[float] = None
    discountRate: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    reviewsCount: Optional[int] = None
    isOutOfStock: bool = False
    users: List[User] = []

    class Config:
        schema_extra = {
            "example": {
                "url": "http://example.com/product",
                "currency": "USD",
                "image": "http://example.com/image.jpg",
                "title": "Example Product",
                "currentPrice": 19.99,
                "originalPrice": 29.99,
                "priceHistory": [
                    {"price": 19.99, "date": "2024-10-21T00:00:00"},
                    {"price": 24.99, "date": "2024-10-20T00:00:00"}
                ],
                "lowestPrice": 19.99,
                "highestPrice": 29.99,
                "averagePrice": 24.99,
                "discountRate": 33.33,
                "description": "This is an example product.",
                "category": "Electronics",
                "reviewsCount": 100,
                "isOutOfStock": False,
                "users": [
                    {"email": "user@example.com"}
                ]
            }
        }
