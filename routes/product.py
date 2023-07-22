from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from database.database import Product
from models.product import ProductCreate, ProductUpdate
from dependency import get_current_user
from serializers.product import products_serializer, product_serializer
from utils import validator

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


# Get Product By Id -> GET /api/product/{id}
@router.get("/{id}")
async def get_product_by_id(id: str, user: dict = Depends(get_current_user)):
    product = await Product.find_one({"_id": ObjectId(id)})

    if product:
        return JSONResponse(status_code=200, content={"product": product_serializer(product)})

    return JSONResponse(status_code=400, content={"error": "Product could not be fetched"})


# Update Product By Id -> PUT /api/product/{id}
@router.put("/{id}")
async def update_product_by_id(id: str, product: ProductUpdate, user: dict = Depends(get_current_user)):
    
    productExists = await Product.find_one({"_id": ObjectId(id)})
    if not productExists:
        return JSONResponse(status_code=400, content={"error": "Product does not exist"})

    productUpdated = await Product.update_one({"_id": ObjectId(id)}, {"$set": validator.remove_none_values(product.dict())})

    if productUpdated:
        return JSONResponse(status_code=200, content={"message": "Product updated successfully"})

    return JSONResponse(status_code=400, content={"error": "Product could not be updated"})