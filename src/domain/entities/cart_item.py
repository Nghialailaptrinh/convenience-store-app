from dataclasses import dataclass
from uuid import UUID


@dataclass
class CartItem:
    product_id: UUID
    quantity: int
