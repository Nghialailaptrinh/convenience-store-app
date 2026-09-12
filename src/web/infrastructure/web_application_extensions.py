from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def use_storefront(app: FastAPI, wwwroot: Path) -> None:
    app.mount("/static", StaticFiles(directory=wwwroot), name="static")

    @app.get("/", include_in_schema=False)
    def storefront():
        return FileResponse(wwwroot / "index.html")
