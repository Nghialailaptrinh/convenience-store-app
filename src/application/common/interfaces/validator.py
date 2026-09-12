from typing import Protocol


class Validator[TRequest](Protocol):
    def validate(self, request: TRequest) -> None: ...
