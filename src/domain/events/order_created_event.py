from dataclasses import dataclass

from domain.common.base_event import BaseEvent
from domain.entities.order import Order


@dataclass(frozen=True)
class OrderCreatedEvent(BaseEvent):
    """Example event contract; the current shopping flow does not publish events."""

    order: Order
