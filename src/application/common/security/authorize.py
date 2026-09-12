from dataclasses import dataclass


@dataclass(frozen=True)
class Authorize:
    """Declarative contract for future authorization; not enforced in this demo."""

    roles: tuple[str, ...] = ()
    policy: str | None = None
