from dataclasses import dataclass, field
from uuid import UUID

from src.domain.entities.cart_item import CartItem


@dataclass
class Cart:
    id: UUID
    customer_id: UUID
    items: list[CartItem] = field(default_factory=list)
