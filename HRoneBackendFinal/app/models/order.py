from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

# Custom ObjectId field for MongoDB compatibility
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator):
        return {"type": "string"}

# Order item model
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Order model
class OrderModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    items: List[OrderItem] = Field(...)
    total_amount: float = Field(..., gt=0)
    shipping_address: str = Field(...)
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "items": [
                    {
                        "product_id": "product123",
                        "product_name": "Smartphone",
                        "quantity": 1,
                        "price": 999.99
                    }
                ],
                "total_amount": 999.99,
                "shipping_address": "123 Main St, City, Country",
                "status": "pending"
            }
        }
    }

# Order creation model
class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: float = Field(..., gt=0)
    shipping_address: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "items": [
                    {
                        "product_id": "product123",
                        "product_name": "Smartphone",
                        "quantity": 1,
                        "price": 999.99
                    }
                ],
                "total_amount": 999.99,
                "shipping_address": "123 Main St, City, Country"
            }
        }
    }

# Order response model
class OrderResponse(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    items: List[OrderItem]
    total_amount: float
    shipping_address: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Order list response model
class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    limit: int
    offset: int