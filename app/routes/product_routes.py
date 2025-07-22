from flask import Blueprint, request, jsonify, abort
from bson import ObjectId
from ..database.connection import product_collection

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/', methods=['POST'])
def create_product():
    """
    Create a new product
    """
    try:
        # Get the product data from the request
        product_data = request.json
        
        # Insert the product into the database
        result = product_collection.insert_one(product_data)
        
        # Get the created product from the database
        created_product = product_collection.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string for JSON serialization
        created_product["_id"] = str(created_product["_id"])
        
        return jsonify(created_product), 201
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/', methods=['GET'])
def get_products():
    """
    Get all products with optional filtering
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', default=10, type=int)
        skip = request.args.get('skip', default=0, type=int)
        
        # Query the database
        cursor = product_collection.find().skip(skip).limit(limit)
        
        # Convert the cursor to a list
        products = list(cursor)
        
        # Convert ObjectId to string for JSON serialization
        for product in products:
            product["_id"] = str(product["_id"])
        
        return jsonify({
            "products": products,
            "total": product_collection.count_documents({}),
            "limit": limit,
            "skip": skip
        })
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a product by ID
    """
    try:
        # Validate the product ID
        if not ObjectId.is_valid(product_id):
            abort(400, description="Invalid product ID")
        
        # Query the database
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        
        # Check if the product exists
        if not product:
            abort(404, description="Product not found")
        
        # Convert ObjectId to string for JSON serialization
        product["_id"] = str(product["_id"])
        
        return jsonify(product)
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a product by ID
    """
    try:
        # Validate the product ID
        if not ObjectId.is_valid(product_id):
            abort(400, description="Invalid product ID")
        
        # Get the product data from the request
        product_data = request.json
        
        # Update the product in the database
        result = product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_data}
        )
        
        # Check if the product exists
        if result.matched_count == 0:
            abort(404, description="Product not found")
        
        # Get the updated product from the database
        updated_product = product_collection.find_one({"_id": ObjectId(product_id)})
        
        # Convert ObjectId to string for JSON serialization
        updated_product["_id"] = str(updated_product["_id"])
        
        return jsonify(updated_product)
    except Exception as e:
        abort(500, description=str(e))

@bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product by ID
    """
    try:
        # Validate the product ID
        if not ObjectId.is_valid(product_id):
            abort(400, description="Invalid product ID")
        
        # Delete the product from the database
        result = product_collection.delete_one({"_id": ObjectId(product_id)})
        
        # Check if the product exists
        if result.deleted_count == 0:
            abort(404, description="Product not found")
        
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        abort(500, description=str(e))