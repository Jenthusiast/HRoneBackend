# E-commerce API

This is a FastAPI-based e-commerce API built for the HROne Backend Intern Hiring Task. The API provides endpoints for managing products and orders in an e-commerce application similar to Flipkart/Amazon.

## Tech Stack

- Python 3.10+ with FastAPI
- MongoDB with Motor (async MongoDB driver)
- Uvicorn ASGI server

## Project Structure

```
.
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── order.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── order.py
│   ├── __init__.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

## API Endpoints

### Products

- **Create Product**
  - Endpoint: `/products`
  - Method: `POST`
  - Status Code: `201 (CREATED)`

- **List Products**
  - Endpoint: `/products`
  - Method: `GET`
  - Optional Query Parameters:
    - `name`: regex/partial search
    - `size`: filter products by size
    - `limit`: number of documents to return
    - `offset`: number of documents to skip (pagination, sorted by `_id`)
  - Status Code: `200 (OK)`

### Orders

- **Create Order**
  - Endpoint: `/orders`
  - Method: `POST`
  - Status Code: `201 (CREATED)`

- **Get List of Orders**
  - Endpoint: `/orders/<user_id>`
  - Method: `GET`
  - Optional Query Parameters:
    - `limit`: number of documents to return
    - `offset`: number of documents to skip (pagination, sorted by `_id`)
  - Status Code: `200 (OK)`

## Setup and Installation

1. Clone the repository

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure MongoDB
   - Create a MongoDB Atlas M0 free cluster
   - Update the `.env` file with your MongoDB connection string
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
   MONGODB_DB_NAME=ecommerce
   ```

4. Run the application
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Deployment

This application can be deployed to platforms like Render or Railway using their free plans. Make sure to set up the environment variables for MongoDB connection in the deployment platform.

## Testing

You can test the API using the Swagger UI documentation or tools like Postman or curl.

## Author

Created for HROne Backend Intern Hiring Task.