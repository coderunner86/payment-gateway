from app.user.router import router as user_router
from app.product.router import router as product_router
from app.payment.router import router as payment_router

routers = [
    user_router,
    product_router,
    payment_router,
]
