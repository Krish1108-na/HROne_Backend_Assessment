from fastapi import APIRouter, Body, Path, HTTPException, status
from database.mongo import db
from bson import ObjectId

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    body: dict = Body(...)
):
    try:
        # Validate presence of userId and items
        user_id = body.get("userId")
        items = body.get("items")

        if not user_id or not isinstance(items, list):
            raise HTTPException(status_code=400, detail="Invalid request body")

        # Convert productId strings to ObjectId
        for item in items:
            item["productId"] = ObjectId(item["productId"])

        result = db.orders.insert_one({
            "userId": user_id,
            "items": items
        })

        return {"id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/{limit}/{offset}", status_code=status.HTTP_200_OK)
def get_orders_by_user(
    user_id: str = Path(...),
    limit: int = Path(...),
    offset: int = Path(...)
):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},  # Sort by _id (ascending)
        {"$skip": offset},
        {"$limit": limit},
        {
            "$unwind": "$items"
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "productDetails"
            }
        },
        {
            "$unwind": "$productDetails"
        },
        {
            "$group": {
                "_id": "$_id",
                "userId": {"$first": "$userId"},
                "items": {
                    "$push": {
                        "productDetails": {
                            "name": "$productDetails.name",
                            "id": {"$toString": "$productDetails._id"}
                        },
                        "qty": "$items.qty"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "items": 1
            }
        }
    ]

    orders = list(db.orders.aggregate(pipeline))

    # Add pagination metadata
    response = {
        "data": orders,
        "page": {
            "next": offset + limit,
            "limit": len(orders),
            "previous": max(offset - limit, 0)
        }
    }

    return response
