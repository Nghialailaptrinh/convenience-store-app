from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    succeeded: bool
    errors: tuple[str, ...] = ()
