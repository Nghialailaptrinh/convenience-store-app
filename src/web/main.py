from fastapi import FastAPI

from src.web.routes.cart import router as cart_router
from src.web.routes.health import router as health_router
from src.web.routes.orders import router as orders_router
from src.web.routes.products import router as products_router

app = FastAPI(title="Convenience Store API", version="0.1.0")
app.include_router(health_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
