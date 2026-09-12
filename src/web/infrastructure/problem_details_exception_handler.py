from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from application.common.exceptions.validation_exception import ValidationException


def add_exception_handlers(app: FastAPI, error_statuses: dict[type[Exception], int]) -> None:
    async def handle_error(request: Request, exc: Exception):
        status = next(code for kind, code in error_statuses.items() if isinstance(exc, kind))
        return JSONResponse(status_code=status, content={"detail": str(exc)})

    async def handle_validation(request: Request, exc: ValidationException):
        return JSONResponse(status_code=422, content={"detail": str(exc), "errors": exc.errors})

    for error in error_statuses:
        app.add_exception_handler(error, handle_error)
    app.add_exception_handler(ValidationException, handle_validation)
