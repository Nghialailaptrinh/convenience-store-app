from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.money import Money


@dataclass
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: Money
