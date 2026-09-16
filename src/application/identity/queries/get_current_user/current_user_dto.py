from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUserDto:
    user_id: str
    email: str
    name: str
