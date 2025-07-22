import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

# MongoDB connection string and database name
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set")
if not DB_NAME:
    raise ValueError("MONGODB_DB_NAME environment variable is not set")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
database = client[DB_NAME]

# Collections
product_collection = database.products
order_collection = database.orders

# Maximum number of connection attempts
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Database connection function
async def connect_to_mongo():
    for attempt in range(MAX_RETRIES):
        try:
            await client.admin.command('ping')
            print(f"Successfully connected to MongoDB on attempt {attempt + 1}!")
            return
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                print(f"Failed to connect to MongoDB after {MAX_RETRIES} attempts: {e}")
                raise HTTPException(
                    status_code=503,
                    detail="Database connection failed. Please try again later."
                )

# Database disconnection function
async def close_mongo_connection():
    try:
        client.close()
        print("MongoDB connection closed successfully.")
    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error closing database connection."
        )

# Health check function
async def check_database_health():
    try:
        await client.admin.command('ping')
        return {"status": "healthy", "message": "Database connection is active"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database health check failed: {str(e)}"
        )