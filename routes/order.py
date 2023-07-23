from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from database.database import Order
from models.order import OrderBase
from dependency import get_current_user
from serializers.order import orders_serializer, order_serializer
from utils import validator

router = APIRouter(prefix="/order")

# Create Product -> POST /api/product
@router.post("/")
async def create_order(order: OrderBase, user: dict = Depends(get_current_user)):

    orderInserted = await Order.insert_one(order.dict())
    if orderInserted:
        return JSONResponse(status_code=200, content={"orderId": str(orderInserted.inserted_id)})

    return JSONResponse(status_code=400, content={"error": "Order could not be created"})

# Get Order By Id -> GET /api/order/{id}
@router.get("/{id}")
async def get_order_by_id(id: str, user: dict = Depends(get_current_user)):
    order = await Order.find_one({"_id": ObjectId(id)})

    if order:
        return JSONResponse(status_code=200, content={"product": order_serializer(order)})

    return JSONResponse(status_code=400, content={"error": "Order could not be fetched"})

# Get All Orders -> GET /api/order
@router.get("/")
async def get_all_orders():
    orders = await Order.find().to_list(100)

    if orders:
        return JSONResponse(status_code=200, content={"orders": orders_serializer(orders)})

    return JSONResponse(status_code=400, content={"error": "Orders could not be fetched"})

