from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from database.database import Basket
from models.basket import BasketBase, BasketUpdate
from dependency import get_current_user
from serializers.basket import basket_serializer, basket_update_serializer
from utils import validator
import pymongo
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

#Get Basket of logged in user -> GET /api/basket/{userId}
@router.get("/myBasket/")
async def get_basket_of_user(user: dict = Depends(get_current_user)):
    basket = await Basket.find_one({"userId": user["id"]})

    if basket:
        return JSONResponse(status_code=200, content={"basket": basket_serializer(basket)})

    return JSONResponse(status_code=400, content={"error": "Basket could not be fetched"})

# Update Basket By Id -> PUT /api/basket/{id}
@router.put("/updateMyBasket/")
async def update_basket_of_user(basket: BasketUpdate, user: dict = Depends(get_current_user)):
    basketExisting = await Basket.find_one({"userId": user["id"]})
    currentBasket = basket.dict()
    existingBasketProducts = basketExisting['products']
    currentBasketProducts = currentBasket['products']
    for itm in currentBasketProducts:
        existing_items = (i for i in existingBasketProducts if i['productId']==itm['productId'])
        for i in existing_items:
            itm['quantity']=i['quantity']+itm['quantity']
            for i in range(len(existingBasketProducts)):
                if existingBasketProducts[i]['productId'] == itm['productId']:
                    del existingBasketProducts[i]
                    break
    updated_basket = existingBasketProducts+currentBasketProducts
    updated_basket_data = {'products':updated_basket}
    basketUpdated = await Basket.update_one({"userId": user["id"]}, {"$set": validator.remove_none_values(updated_basket_data)})
    if basketUpdated:
        return JSONResponse(status_code=200, content={"message": "Basket updated successfully!"})

    return JSONResponse(status_code=400, content={"error": "Basket could not be updated"})






