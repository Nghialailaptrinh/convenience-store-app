import logging
from collections.abc import Callable


class UnhandledExceptionBehaviour:
    def handle[TResponse](
        self, request: object, next_handler: Callable[[], TResponse]
    ) -> TResponse:
        try:
            return next_handler()
        except Exception:
            logging.getLogger(__name__).exception("Request failed: %s", type(request).__name__)
            raise
