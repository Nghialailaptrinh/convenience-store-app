from typing import Protocol
from uuid import UUID

from domain.entities.cart import Cart


class ICartRepository(Protocol):
    def get_by_customer_id(self, customer_id: UUID) -> Cart | None: ...

    def save(self, cart: Cart) -> None: ...
