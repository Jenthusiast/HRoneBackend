import os
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import abort

# Load environment variables
load_dotenv()

# MongoDB connection string and database name
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

# In development mode, we can use a default value if not set
if not MONGODB_URI:
    if os.getenv("ENVIRONMENT") == "development":
        print("WARNING: MONGODB_URI not set, using default localhost connection")
        MONGODB_URI = "mongodb://localhost:27017"
    else:
        raise ValueError("MONGODB_URI environment variable is not set")
        
if not DB_NAME:
    if os.getenv("ENVIRONMENT") == "development":
        print("WARNING: MONGODB_DB_NAME not set, using default 'ecommerce' database")
        DB_NAME = "ecommerce"
    else:
        raise ValueError("MONGODB_DB_NAME environment variable is not set")

# Create a MongoDB client
client = None
database = None

# Collections
product_collection = None
order_collection = None

# Maximum number of connection attempts
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Database connection function
def connect_to_mongo():
    global client, database, product_collection, order_collection
    
    # In development mode, we can proceed even if MongoDB is not available
    if os.getenv("ENVIRONMENT") == "development":
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            database = client[DB_NAME]
            
            # Initialize collections
            product_collection = database.products
            order_collection = database.orders
            
            print("Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"Warning: Could not connect to MongoDB: {e}")
            print("Running in development mode without database connection.")
            return False
    else:
        # In production, we need to retry and ensure connection
        for attempt in range(MAX_RETRIES):
            try:
                client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
                client.admin.command('ping')
                database = client[DB_NAME]
                
                # Initialize collections
                product_collection = database.products
                order_collection = database.orders
                
                print(f"Successfully connected to MongoDB on attempt {attempt + 1}!")
                return True
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Connection attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"Failed to connect to MongoDB after {MAX_RETRIES} attempts: {e}")
                    abort(503, description="Database connection failed. Please try again later.")

# Database disconnection function
def close_mongo_connection():
    global client
    if client:
        try:
            client.close()
            print("MongoDB connection closed successfully.")
        except Exception as e:
            print(f"Error closing MongoDB connection: {e}")
            if os.getenv("ENVIRONMENT") != "development":
                abort(500, description="Error closing database connection.")

# Health check function
def check_database_health():
    if os.getenv("ENVIRONMENT") == "development" and not client:
        return {"status": "development", "message": "Running in development mode without database"}
    
    try:
        if client:
            client.admin.command('ping')
            return {"status": "healthy", "message": "Database connection is active"}
        return {"status": "unknown", "message": "Database client not initialized"}
    except Exception as e:
        if os.getenv("ENVIRONMENT") == "development":
            print(f"Database health check failed: {str(e)}")
            return {"status": "error", "message": f"Database health check failed: {str(e)}"}
        else:
            abort(503, description=f"Database health check failed: {str(e)}")