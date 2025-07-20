**HROne Backend Task - Product and Order API**

A complete backend API built with FastAPI and MongoDB, supporting creation and retrieval of products and orders. Includes flexible filtering, pagination, and data validation using Pydantic models.

**FEATURES**
1) Product APIs
(A) Create Product
(B) Validates name, price, and size quantity.
(C) Accepts multiple sizes per product.

2) List Products
(A) Supports filtering by name (partial match), size, pagination (limit, offset).

3) Order APIs
(A) Create Order
(B) Accepts multiple products with quantities.
(C) Saves order against a user ID.
(D) List Orders by User
(E) Includes joined product details per order.
(F) Supports pagination via path params (limit, offset).

**PROJECT STRUCTURE**
HROne_Backend_Task/
|
├── main.py                       # FastAPI app instance and route registration
├── database/
│   └── mongo.py                  # MongoDB connection using pymongo
|
├── models/
│   └── product.py                # Pydantic models for input validation
|
├── routes/
│   ├── product_routes.py         # All /products endpoints
│   └── order_routes.py           # All /orders endpoints
|
├── .env                          # Environment config (MongoDB URI, DB name)
└── requirements.txt              # Project dependencies

**Setup Instructions**
1. Clone the Repository
git clone <repo_url>
cd HROne_Backend_Task

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows

3. Install Dependencies
pip install -r requirements.txt

4. Setup Environment Variables
Create a .env file:
MONGO_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/
MONGO_DB=hrone_db

5. Run the Server
uvicorn main:app --reload
Access docs at: http://localhost:8000/docs

**API EXAMPLES**

1) POST /products/
{
  "name": "T-shirt",
  "price": 499.99,
  "size": [
    {"size": "M", "quantity": 10},
    {"size": "L", "quantity": 5}
  ]
}

Validation:
A) name not empty, max length 20
B) price ≥ 0
C) quantity ≥ 0

2) GET /products?name=shirt&size=M&limit=2&offset=0
Returns filtered product list with pagination.

3) POST /orders/
{
  "userId": "user_1",
  "items": [
    {"productId": "<product_id>", "qty": 2},
    {"productId": "<product_id>", "qty": 1}
  ]
}
Validation:
A) qty must be ≥ 0

4) GET /orders/user_1/5/0
A) Returns orders placed by user user_1
B) Includes product name and ID inside each order
C) Supports pagination

**TECH STACK**

1) FastAPI
2) Pydantic
3) MongoDB Atlas
4) Uvicorn
5) PyMongo

**FINAL NOTE**

This project was structured with clean modularity, input validation, and MongoDB best practices in mind. It is extensible for future enhancements like user auth, admin dashboards, or analytics.

