from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from application.common.exceptions.use_case_not_implemented import UseCaseNotImplemented
from web.endpoints.cart import router as cart_router
from web.endpoints.health import router as health_router
from web.endpoints.orders import router as orders_router
from web.endpoints.products import router as products_router

app = FastAPI(title="Convenience Store API", version="0.1.0")
app.include_router(health_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.exception_handler(UseCaseNotImplemented)
async def use_case_not_implemented(request: Request, exc: UseCaseNotImplemented) -> JSONResponse:
    return JSONResponse(status_code=501, content={"detail": str(exc)})
