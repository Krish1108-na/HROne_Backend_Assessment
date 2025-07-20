from fastapi import APIRouter, Body, status, Query
from typing import Optional
from database.mongo import db
from bson.objectid import ObjectId
from models.product import ProductCreate
import re

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate = Body(...)):
    result = db.products.insert_one(product.dict())
    return {"_id": str(result.inserted_id)}

@router.get("/", status_code=200)
def get_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: int = Query(10),
    offset: int = Query(0)
):
    query = {}

    # Partial regex search on name
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    # Match if any object in size array has the given size
    if size:
        query["size.size"] = size

    # Fetch total documents matching the filter
    products_cursor = db.products.find(query).skip(offset).limit(limit)

    products = []
    for product in products_cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
        })

    # Prepare pagination object
    response = {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(offset - limit, 0)
        }
    }

    return response
