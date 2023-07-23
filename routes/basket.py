from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from database.database import Basket
from models.basket import BasketBase
from dependency import get_current_user
from serializers.basket import basket_serializer
from utils import validator

router = APIRouter(prefix="/basket")

# Create Basket -> POST /api/basket
@router.post("/")
async def create_basket(basket: BasketBase, user: dict = Depends(get_current_user)):

    basketInserted = await Basket.insert_one(basket.dict())
    if basketInserted:
        return JSONResponse(status_code=200, content={"basketId": str(basketInserted.inserted_id)})

    return JSONResponse(status_code=400, content={"error": "Basket could not be created"})

# Get Basket By Id -> GET /api/basket/{id}
@router.get("/{id}")
async def get_basket_by_id(id: str, user: dict = Depends(get_current_user)):
    basket = await Basket.find_one({"_id": ObjectId(id)})

    if basket:
        return JSONResponse(status_code=200, content={"basket": basket_serializer(basket)})

    return JSONResponse(status_code=400, content={"error": "Basket could not be fetched"})


# Update Basket By Id -> PUT /api/basket/{id}
@router.put("/{id}")
async def update_basket_by_id(id: str, basket: BasketBase, user: dict = Depends(get_current_user)):

    basketUpdated = await Basket.update_one({"_id": ObjectId(id)}, {"$set": validator.remove_none_values(basket.dict())})

    if basketUpdated:
        return JSONResponse(status_code=200, content={"message": "Basket updated successfully"})

    return JSONResponse(status_code=400, content={"error": "Basket could not be updated"})