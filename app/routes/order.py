from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from bson import ObjectId
from ..models.order import OrderCreate, OrderResponse, OrderListResponse
from ..database.connection import order_collection, product_collection

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """
    Create a new order
    """
    # Convert the order model to a dictionary
    order_dict = order.dict()
    
    # Validate product existence and update stock
    for item in order.items:
        product_id = item.product_id
        quantity = item.quantity
        
        # Check if product exists and has enough stock
        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with ID {product_id} not found"
            )
        
        if product["stock"] < quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for product {product['name']}"
            )
        
        # Update product stock
        await product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": -quantity}}
        )
    
    # Insert the order into the database
    result = await order_collection.insert_one(order_dict)
    
    # Get the created order from the database
    created_order = await order_collection.find_one({"_id": result.inserted_id})
    
    if created_order is None:
        raise HTTPException(status_code=404, detail="Order creation failed")
    
    return created_order

@router.get("/orders/{user_id}", response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def list_orders(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List orders for a specific user with pagination
    """
    # Build the query filter
    query = {"user_id": user_id}
    
    # Get the total count of matching orders
    total = await order_collection.count_documents(query)
    
    # Get the orders with pagination
    cursor = order_collection.find(query).sort("_id", 1).skip(offset).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    # Return the orders list response
    return {
        "orders": orders,
        "total": total,
        "limit": limit,
        "offset": offset
    }