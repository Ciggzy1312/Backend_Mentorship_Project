from fastapi import APIRouter, Depends
from dependency import get_current_user

router = APIRouter(prefix="/user")

# Get User Profile Details -> POST /api/user/me
@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return user