from pydantic import BaseModel
from bson import ObjectId

class BasketProductInfo(BaseModel):
    productId: str
    quantity: int

class BasketBase(BaseModel):
    userId: str | None = None
    products: list[BasketProductInfo] | None = None


