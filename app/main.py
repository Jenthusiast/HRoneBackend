from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import product, order
from .database.connection import connect_to_mongo, close_mongo_connection

# Create FastAPI app
app = FastAPI(
    title="E-commerce API",
    description="E-commerce API for HROne Backend Intern Hiring Task",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product.router, tags=["Products"])
app.include_router(order.router, tags=["Orders"])

# Startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the E-commerce API"}