from fastapi import APIRouter

from routes import auth, user, product

router = APIRouter(prefix="/api")

router.include_router(auth.router)

router.include_router(user.router)

router.include_router(product.router)