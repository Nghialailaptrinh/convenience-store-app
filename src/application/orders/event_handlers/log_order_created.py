import logging

from domain.events.order_created_event import OrderCreatedEvent


class LogOrderCreated:
    """Example event handler, reserved until domain-event dispatch is enabled."""

    def handle(self, event: OrderCreatedEvent) -> None:
        logging.getLogger(__name__).info("Order created: %s", event.order.id)
