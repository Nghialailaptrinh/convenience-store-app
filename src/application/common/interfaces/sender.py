from typing import Protocol

from application.common.interfaces.request import Request


class Sender(Protocol):
    def send[TResponse](self, request: Request[TResponse]) -> TResponse: ...
