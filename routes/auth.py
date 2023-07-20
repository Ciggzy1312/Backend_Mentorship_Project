from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from bson import ObjectId

from models.user import UserCreate, UserLogin
from database.database import User
from utils import password, token
from serializers import user

router = APIRouter(prefix="/auth")

# Register User -> POST /api/auth/register
@router.post("/register")
async def register(payload: UserCreate):
    print(payload)
    if(payload.name == "" or payload.email == "" or payload.password == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    userExists = await User.find_one({"email": payload.email})
    print(userExists)
    if userExists:
        return JSONResponse(status_code=400, content={"message": "User with this email already exists"})

    payload.password = password.hashPassword(payload.password)

    userInserted = await User.insert_one(payload.dict())

    return JSONResponse(status_code=200, content={"message": "User registered successfully", "userId": str(userInserted.inserted_id)})


# Login User -> POST /api/auth/login
@router.post("/login")
async def login(payload: UserLogin):
    if payload.email == "" or payload.password == "":
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    userExists = await User.find_one({"email": payload.email})
    if not userExists:
        return JSONResponse(status_code=400, content={"message": "User with this email does not exist"})

    if not password.verifyPassword(payload.password, userExists["password"]):
        return JSONResponse(status_code=400, content={"message": "Incorrect password"})

    authToken = await token.generateToken(user.user_serializer(userExists), timedelta(minutes=15))

    template_response = JSONResponse(status_code=200, content={"message": "User logged in successfully"})
    template_response.set_cookie(key="token", value=authToken, httponly=True)

    return template_response