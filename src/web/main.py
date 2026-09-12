"""Composition root: the only Web module that selects concrete adapters."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from application.common.exceptions.not_found import NotFoundError
from application.common.exceptions.payment_failed import PaymentFailedError
from domain.exceptions.business_rule_error import BusinessRuleError
from infrastructure.dependency_injection import create_demo_dependencies
from web.endpoints.cart import router as cart_router
from web.endpoints.health import router as health_router
from web.endpoints.orders import router as orders_router
from web.endpoints.products import router as products_router

STATIC = Path(__file__).parent / "static"


def create_app(database_url: str | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine, app.state.uow_factory, app.state.payment = create_demo_dependencies(database_url)
        try:
            yield
        finally:
            engine.dispose()

    app = FastAPI(title="Convenience Store Demo", version="0.2.0", lifespan=lifespan)
    for router in (health_router, products_router, cart_router, orders_router):
        app.include_router(router)

    async def business_error(request: Request, exc: BusinessRuleError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    async def not_found(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    async def payment_failed(request: Request, exc: PaymentFailedError):
        return JSONResponse(status_code=402, content={"detail": str(exc)})

    app.add_exception_handler(BusinessRuleError, business_error)
    app.add_exception_handler(NotFoundError, not_found)
    app.add_exception_handler(PaymentFailedError, payment_failed)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/", include_in_schema=False)
    def storefront():
        return FileResponse(STATIC / "index.html")

    return app


app = create_app()
