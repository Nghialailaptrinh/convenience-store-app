from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CartItemDto:
    product_id: UUID
    quantity: int
