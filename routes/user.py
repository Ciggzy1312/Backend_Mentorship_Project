import json
from datetime import timedelta
from fastapi import APIRouter, Depends
from bson import ObjectId
from dependency import get_current_user
from fastapi.responses import JSONResponse

from database.database import redis_client
from database.database import Product, User
from serializers.product import products_serializer
from serializers.user import user_serializer

router = APIRouter(prefix="/user")

# Get User Profile Details -> POST /api/user/me
@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    # Check if user is in Redis
    userExist = redis_client.hget("user", user["id"])

    if userExist:
        print("Serving from cache in Redis")
        return JSONResponse(status_code=200, content=json.loads(userExist))

    # If not in Redis, get from MongoDB
    user1 = await User.find_one({"_id": ObjectId(user["id"])})
    if not user1:
        return JSONResponse(status_code=400, content={"error": "User does not exist"})

    redis_client.hset("user", str(ObjectId(user1["_id"])), json.dumps(user_serializer(user1)))
    redis_client.expire("user", timedelta(seconds=10))

    return JSONResponse(status_code=200, content=user_serializer(user1))


# Get Products By User -> GET /api/user/products
@router.get("/products")
async def get_products_by_user(user: dict = Depends(get_current_user)):
    products = await Product.find({"created_by": user["id"]}).to_list(100)

    if products:
        return JSONResponse(status_code=200, content={"products": products_serializer(products)})

    return JSONResponse(status_code=400, content={"error": "Products could not be fetched"})