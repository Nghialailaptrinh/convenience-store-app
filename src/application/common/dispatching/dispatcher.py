from collections.abc import Callable
from typing import Any, cast

from application.common.behaviours.validation_behaviour import ValidationBehaviour
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.interfaces.validator import Validator


class Dispatcher:
    """Dispatch to a fresh handler; no dependency on HTTP or persistence adapters."""

    def __init__(self) -> None:
        self._factories: dict[type, Callable[[], RequestHandler[Any, Any]]] = {}
        self._validators: dict[type, Validator[Any]] = {}
        self._validation = ValidationBehaviour()

    def register[TResponse](
        self,
        request_type: type[Request[TResponse]],
        factory: Callable[[], RequestHandler[Any, TResponse]],
        validator: Validator[Any] | None = None,
    ) -> None:
        if request_type in self._factories:
            raise ValueError(f"Handler already registered for {request_type.__name__}")
        self._factories[request_type] = factory
        if validator is not None:
            self._validators[request_type] = validator

    def send[TResponse](self, request: Request[TResponse]) -> TResponse:
        factory = self._factories.get(type(request))
        if factory is None:
            raise LookupError(f"No handler registered for {type(request).__name__}")
        self._validation.validate(request, self._validators.get(type(request)))
        handler = cast(RequestHandler[Request[TResponse], TResponse], factory())
        return handler.handle(request)
