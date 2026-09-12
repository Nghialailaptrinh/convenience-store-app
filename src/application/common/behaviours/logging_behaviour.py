import logging
from collections.abc import Callable


class LoggingBehaviour:
    def handle[TResponse](
        self, request: object, next_handler: Callable[[], TResponse]
    ) -> TResponse:
        logging.getLogger(__name__).debug("Handling %s", type(request).__name__)
        return next_handler()
