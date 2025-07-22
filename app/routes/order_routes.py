from flask import Blueprint, request, jsonify, abort
from bson import ObjectId
from ..database.connection import order_collection, product_collection

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
def create_order():
    """
    Create a new order
    """
    try:
        # Get the order data from the request
        order_data = request.json
        
        # Validate products in the order
        if 'products' not in order_data or not order_data['products']:
            abort(400, description="Order must contain at least one product")
        
        # Check if all products exist and calculate total price
        total_price = 0
        for product_item in order_data['products']:
            product_id = product_item.get('product_id')
            quantity = product_item.get('quantity', 1)
            
            if not product_id or not ObjectId.is_valid(product_id):
                abort(400, description=f"Invalid product ID: {product_id}")
            
            product = product_collection.find_one({"_id": ObjectId(product_id)})
            if not product:
                abort(404, description=f"Product not found: {product_id}")
            
            # Calculate item price
            item_price = product.get('price', 0) * quantity
            product_item['price'] = product.get('price', 0)
            product_item['name'] = product.get('name', '')
            product_item['total'] = item_price
            
            # Add to total price
            total_price += item_price
        
        # Add total price to order
        order_data['total_price'] = total_price
        
        # Add order date if not provided
        if 'order_date' not in order_data:
            from datetime import datetime
            order_data['order_date'] = datetime.utcnow().isoformat()
        
        # Insert the order into the database
        result = order_collection.insert_one(order_data)
        
        # Get the created order from the database
        created_order = order_collection.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string for JSON serialization
        created_order["_id"] = str(created_order["_id"])
        
        return jsonify(created_order), 201
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/', methods=['GET'])
def get_orders():
    """
    Get all orders with optional filtering
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', default=10, type=int)
        skip = request.args.get('skip', default=0, type=int)
        
        # Query the database
        cursor = order_collection.find().skip(skip).limit(limit)
        
        # Convert the cursor to a list
        orders = list(cursor)
        
        # Convert ObjectId to string for JSON serialization
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return jsonify({
            "orders": orders,
            "total": order_collection.count_documents({}),
            "limit": limit,
            "skip": skip
        })
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get an order by ID
    """
    try:
        # Validate the order ID
        if not ObjectId.is_valid(order_id):
            abort(400, description="Invalid order ID")
        
        # Query the database
        order = order_collection.find_one({"_id": ObjectId(order_id)})
        
        # Check if the order exists
        if not order:
            abort(404, description="Order not found")
        
        # Convert ObjectId to string for JSON serialization
        order["_id"] = str(order["_id"])
        
        return jsonify(order)
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Update an order by ID
    """
    try:
        # Validate the order ID
        if not ObjectId.is_valid(order_id):
            abort(400, description="Invalid order ID")
        
        # Get the order data from the request
        order_data = request.json
        
        # Recalculate total price if products are updated
        if 'products' in order_data and order_data['products']:
            total_price = 0
            for product_item in order_data['products']:
                product_id = product_item.get('product_id')
                quantity = product_item.get('quantity', 1)
                
                if not product_id or not ObjectId.is_valid(product_id):
                    abort(400, description=f"Invalid product ID: {product_id}")
                
                product = product_collection.find_one({"_id": ObjectId(product_id)})
                if not product:
                    abort(404, description=f"Product not found: {product_id}")
                
                # Calculate item price
                item_price = product.get('price', 0) * quantity
                product_item['price'] = product.get('price', 0)
                product_item['name'] = product.get('name', '')
                product_item['total'] = item_price
                
                # Add to total price
                total_price += item_price
            
            # Add total price to order
            order_data['total_price'] = total_price
        
        # Update the order in the database
        result = order_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": order_data}
        )
        
        # Check if the order exists
        if result.matched_count == 0:
            abort(404, description="Order not found")
        
        # Get the updated order from the database
        updated_order = order_collection.find_one({"_id": ObjectId(order_id)})
        
        # Convert ObjectId to string for JSON serialization
        updated_order["_id"] = str(updated_order["_id"])
        
        return jsonify(updated_order)
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an order by ID
    """
    try:
        # Validate the order ID
        if not ObjectId.is_valid(order_id):
            abort(400, description="Invalid order ID")
        
        # Delete the order from the database
        result = order_collection.delete_one({"_id": ObjectId(order_id)})
        
        # Check if the order exists
        if result.deleted_count == 0:
            abort(404, description="Order not found")
        
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        abort(500, description=str(e))