from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database.database import Product
from models.product import ProductCreate

from dependency import get_current_user
from serializers.product import products_serializer


router = APIRouter(prefix="/product")

# Create Product -> POST /api/product
@router.post("/")
async def create_product(product: ProductCreate, user: dict = Depends(get_current_user)):
    if product.name == "" or product.description == "" or product.price == "" or product.quantity == "":
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})
        
    product.created_by = user["id"]

    productInserted = await Product.insert_one(product.dict())

    if productInserted:
        return JSONResponse(status_code=200, content={"message": "Product created successfully", "productId": str(productInserted.inserted_id)})

    return JSONResponse(status_code=400, content={"error": "Product could not be created"})


# Get All Products -> GET /api/product
@router.get("/")
async def get_all_products():
    products = await Product.find().to_list(100)

    if products:
        return JSONResponse(status_code=200, content={"products": products_serializer(products)})

    return JSONResponse(status_code=400, content={"error": "Products could not be fetched"})