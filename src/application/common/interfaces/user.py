from typing import Protocol


class User(Protocol):
    @property
    def id(self) -> str | None: ...
