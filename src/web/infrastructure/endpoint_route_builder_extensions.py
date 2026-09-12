from fastapi import APIRouter, FastAPI


def map_endpoints(app: FastAPI, *routers: APIRouter) -> None:
    for router in routers:
        app.include_router(router)
