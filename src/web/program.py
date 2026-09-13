"""Composition root, corresponding to the template's Web/Program.cs."""

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from application.common.exceptions.invalid_credentials import InvalidCredentialsError
from application.common.exceptions.not_found import NotFoundError
from application.common.exceptions.payment_failed import PaymentFailedError
from application.common.exceptions.registration_failed import RegistrationFailedError
from domain.exceptions.business_rule_error import BusinessRuleError
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service
from web.endpoints.carts import router as carts_router
from web.endpoints.health import router as health_router
from web.endpoints.identity import router as identity_router
from web.endpoints.orders import router as orders_router
from web.endpoints.products import router as products_router
from web.infrastructure.endpoint_route_builder_extensions import map_endpoints
from web.infrastructure.problem_details_exception_handler import add_exception_handlers
from web.infrastructure.web_application_extensions import use_storefront

WEB_ROOT = Path(__file__).parent


def create_app(database_url: str | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = json.loads((WEB_ROOT / "appsettings.json").read_text(encoding="utf-8"))
        connection = (
            database_url
            or os.getenv("DATABASE_URL")
            or settings["ConnectionStrings"]["DefaultConnection"]
        )
        engine, app.state.context_factory, app.state.payment = create_demo_dependencies(connection)
        try:
            app.state.identity = create_identity_service(engine)
            yield
        finally:
            engine.dispose()

    app = FastAPI(title="Convenience Store Demo", version="0.2.0", lifespan=lifespan)
    map_endpoints(app, health_router, products_router, carts_router, orders_router, identity_router)
    add_exception_handlers(
        app,
        {
            BusinessRuleError: 409,
            NotFoundError: 404,
            PaymentFailedError: 402,
            InvalidCredentialsError: 401,
            RegistrationFailedError: 409,
        },
    )
    use_storefront(app, WEB_ROOT / "wwwroot")
    return app


app = create_app()
