from pydantic import BaseModel
from bson import ObjectId

class BasketBase(BaseModel):
    userId: str | None = None
    products: list | None = None

