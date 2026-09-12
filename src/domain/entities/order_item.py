from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: Decimal
