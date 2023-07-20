from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.user import UserCreate
from database.database import User
from utils.password import hashPassword

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(payload: UserCreate):
    print(payload)
    if(payload.name == "" or payload.email == "" or payload.password == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    userExists = await User.find_one({"email": payload.email})
    print(userExists)
    if userExists:
        return JSONResponse(status_code=400, content={"message": "User with this email already exists"})

    payload.password = hashPassword(payload.password)

    userInserted = await User.insert_one(payload.dict())

    return JSONResponse(status_code=200, content={"message": "User registered successfully", "userId": str(userInserted.inserted_id)})