from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from bson import ObjectId
from ..models.product import ProductCreate, ProductResponse, ProductListResponse
from ..database.connection import product_collection

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product
    """
    # Convert the product model to a dictionary
    product_dict = product.dict()
    
    # Insert the product into the database
    result = await product_collection.insert_one(product_dict)
    
    # Get the created product from the database
    created_product = await product_collection.find_one({"_id": result.inserted_id})
    
    if created_product is None:
        raise HTTPException(status_code=404, detail="Product creation failed")
    
    return created_product

@router.get("/products", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List products with optional filtering
    """
    # Build the query filter
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Case-insensitive regex search
    
    if size:
        query["size"] = size
    
    # Get the total count of matching products
    total = await product_collection.count_documents(query)
    
    # Get the products with pagination
    cursor = product_collection.find(query).sort("_id", 1).skip(offset).limit(limit)
    products = await cursor.to_list(length=limit)
    
    # Return the products list response
    return {
        "products": products,
        "total": total,
        "limit": limit,
        "offset": offset
    }