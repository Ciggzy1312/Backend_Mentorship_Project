from fastapi import APIRouter

from routes import auth, user, product, basket, order

router = APIRouter(prefix="/api")

router.include_router(auth.router)

router.include_router(user.router)

router.include_router(product.router)

router.include_router(basket.router)

router.include_router(order.router)