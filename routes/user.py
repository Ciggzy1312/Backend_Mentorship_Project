from fastapi import APIRouter, Depends
from dependency import get_current_user
from fastapi.responses import JSONResponse

from database.database import Product
from serializers.product import products_serializer

router = APIRouter(prefix="/user")

# Get User Profile Details -> POST /api/user/me
@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return user


# Get Products By User -> GET /api/user/products
@router.get("/products")
async def get_products_by_user(user: dict = Depends(get_current_user)):
    products = await Product.find({"created_by": user["id"]}).to_list(100)

    if products:
        return JSONResponse(status_code=200, content={"products": products_serializer(products)})

    return JSONResponse(status_code=400, content={"error": "Products could not be fetched"})