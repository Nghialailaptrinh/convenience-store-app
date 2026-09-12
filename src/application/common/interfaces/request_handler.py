from typing import Protocol


class RequestHandler[TRequest, TResponse](Protocol):
    """Handle one request; dependencies belong in the concrete constructor."""

    def handle(self, request: TRequest) -> TResponse: ...
