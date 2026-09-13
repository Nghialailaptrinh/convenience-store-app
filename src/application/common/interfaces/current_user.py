from typing import Protocol


class ICurrentUser(Protocol):
    @property
    def user_id(self) -> str | None: ...
