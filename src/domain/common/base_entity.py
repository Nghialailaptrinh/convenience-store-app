from dataclasses import dataclass, field
from uuid import UUID

from domain.common.base_event import BaseEvent


@dataclass
class BaseEntity:
    """Optional entity base with an explicit, framework-free event collection."""

    id: UUID
    _domain_events: list[BaseEvent] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    @property
    def domain_events(self) -> tuple[BaseEvent, ...]:
        return tuple(self._domain_events)

    def add_domain_event(self, event: BaseEvent) -> None:
        self._domain_events.append(event)

    def remove_domain_event(self, event: BaseEvent) -> None:
        if event in self._domain_events:
            self._domain_events.remove(event)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()
