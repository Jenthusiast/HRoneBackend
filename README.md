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
├── render.yaml
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

### Health Check

- **Health Check**
  - Endpoint: `/health`
  - Method: `GET`
  - Returns the health status of the API and database connection
  - Status Code: `200 (OK)` or `503 (Service Unavailable)`

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
   python run.py
   ```

5. Access the API documentation
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Deployment to Render

### Option 1: Manual Deployment

1. Create a new Web Service on Render
   - Sign up or log in to [Render](https://render.com/)
   - Click on "New +" and select "Web Service"

2. Connect your repository
   - Connect your GitHub/GitLab account
   - Select the repository containing this project

3. Configure the service
   - Name: `hrone-backend` (or your preferred name)
   - Environment: `Python 3`
   - Region: Choose the closest to your users
   - Branch: `main` (or your default branch)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`

4. Add environment variables
   - Click on "Environment" tab
   - Add the following environment variables:
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `MONGODB_DB_NAME`: Your database name (e.g., `ecommerce`)

5. Deploy the service
   - Click on "Create Web Service"
   - Wait for the deployment to complete

### Option 2: Using Blueprint (render.yaml)

1. Push the repository with the `render.yaml` file to GitHub/GitLab

2. Create a new Blueprint on Render
   - Sign up or log in to [Render](https://render.com/)
   - Navigate to "Blueprints" section
   - Click on "New Blueprint Instance"

3. Connect your repository
   - Connect your GitHub/GitLab account
   - Select the repository containing this project

4. Configure the blueprint
   - The configuration will be automatically loaded from `render.yaml`
   - Update the environment variables as needed

5. Deploy the blueprint
   - Click on "Apply"
   - Wait for the deployment to complete

### MongoDB Atlas Setup

1. Create a MongoDB Atlas account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

2. Create a new cluster (M0 free tier is sufficient)

3. Set up database access
   - Create a database user with password authentication
   - Note down the username and password

4. Set up network access
   - Add your IP address to the IP Access List
   - For Render deployment, allow access from anywhere (0.0.0.0/0)

5. Get your connection string
   - Click on "Connect" for your cluster
   - Select "Connect your application"
   - Copy the connection string and replace `<username>`, `<password>`, and `<dbname>` with your values

## Testing

You can test the API using the Swagger UI documentation or tools like Postman or curl.

## Author

Created for HROne Backend Intern Hiring Task.