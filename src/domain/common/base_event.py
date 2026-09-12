from dataclasses import dataclass


@dataclass(frozen=True)
class BaseEvent:
    """Base for domain facts; publishing belongs to an outer layer."""
