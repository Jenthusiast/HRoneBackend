from flask import Flask, jsonify
from flask_cors import CORS
from .database.connection import connect_to_mongo, close_mongo_connection, check_database_health

# Create Flask app
app = Flask(__name__)

# Configure app
app.config.update(
    TITLE="E-commerce API",
    DESCRIPTION="E-commerce API for HROne Backend Intern Hiring Task",
    VERSION="1.0.0"
)

# Add CORS
CORS(app)

# Import routes
from .routes import product_routes, order_routes

# Register blueprints
app.register_blueprint(product_routes.bp)
app.register_blueprint(order_routes.bp)

# Database connection setup
@app.before_request
def setup_db():
    # Only connect once
    if not hasattr(app, 'db_initialized'):
        connect_to_mongo()
        app.db_initialized = True

@app.teardown_appcontext
def teardown_db(exception):
    close_mongo_connection()

# Root endpoint
@app.route('/')
def read_root():
    return jsonify({"message": "Welcome to the E-commerce API"})

# Health check endpoint
@app.route('/health')
def health_check():
    db_health = check_database_health()
    return jsonify({
        "status": "healthy",
        "database": db_health,
        "api": {"status": "running"}
    })