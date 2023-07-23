from pydantic import BaseModel
from bson import ObjectId

class OrderBase(BaseModel):
    basketId: str