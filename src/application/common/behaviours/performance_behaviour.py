import logging
from collections.abc import Callable
from time import perf_counter


class PerformanceBehaviour:
    def handle[TResponse](
        self, request: object, next_handler: Callable[[], TResponse]
    ) -> TResponse:
        started = perf_counter()
        try:
            return next_handler()
        finally:
            elapsed = perf_counter() - started
            if elapsed > 0.5:
                logging.getLogger(__name__).warning(
                    "Slow request %s: %.3fs", type(request).__name__, elapsed
                )
