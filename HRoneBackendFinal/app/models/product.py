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

# Product model
class ProductModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(..., gt=0)
    category: str = Field(...)
    size: Optional[str] = Field(None)
    stock: int = Field(..., ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "name": "Smartphone",
                "description": "Latest smartphone with advanced features",
                "price": 999.99,
                "category": "Electronics",
                "size": "Medium",
                "stock": 50
            }
        }
    }

# Product creation model
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)
    category: str
    size: Optional[str] = None
    stock: int = Field(..., ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Smartphone",
                "description": "Latest smartphone with advanced features",
                "price": 999.99,
                "category": "Electronics",
                "size": "Medium",
                "stock": 50
            }
        }
    }

# Product response model
class ProductResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    description: str
    price: float
    category: str
    size: Optional[str] = None
    stock: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Product list response model
class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    limit: int
    offset: int