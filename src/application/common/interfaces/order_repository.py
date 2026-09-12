from typing import Protocol
from uuid import UUID

from domain.entities.order import Order


class IOrderRepository(Protocol):
    def get_by_id(self, order_id: UUID) -> Order | None: ...

    def save(self, order: Order) -> None: ...
