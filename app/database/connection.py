import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
database = client[DB_NAME]

# Collections
product_collection = database.products
order_collection = database.orders

# Database connection function
async def connect_to_mongo():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Warning: Could not connect to MongoDB: {e}")
        print("The application will continue, but database operations will not work.")
        # Don't raise the exception to allow the app to start without MongoDB

# Database disconnection function
async def close_mongo_connection():
    try:
        client.close()
        print("MongoDB connection closed.")
    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")
        raise