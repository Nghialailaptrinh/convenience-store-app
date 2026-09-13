from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from application.common.exceptions.validation_exception import ValidationException


def add_exception_handlers(app: FastAPI, error_statuses: dict[type[Exception], int]) -> None:
    async def handle_error(request: Request, exc: Exception):
        status = next(code for kind, code in error_statuses.items() if isinstance(exc, kind))
        headers = (
            {"WWW-Authenticate": "Bearer", "Cache-Control": "no-store"} if status == 401 else {}
        )
        return JSONResponse(status_code=status, content={"detail": str(exc)}, headers=headers)

    async def handle_validation(request: Request, exc: ValidationException):
        return JSONResponse(status_code=422, content={"detail": str(exc), "errors": exc.errors})

    async def handle_request_validation(request: Request, exc: RequestValidationError):
        if request.url.path.startswith("/identity/"):
            # FastAPI's default errors include raw input, which may contain passwords.
            errors = [
                {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
                for error in exc.errors()
            ]
            return JSONResponse(status_code=422, content={"detail": errors})
        return await request_validation_exception_handler(request, exc)

    for error in error_statuses:
        app.add_exception_handler(error, handle_error)
    app.add_exception_handler(ValidationException, handle_validation)
    app.add_exception_handler(RequestValidationError, handle_request_validation)
