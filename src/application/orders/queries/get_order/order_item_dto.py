from dataclasses import dataclass
from uuid import UUID

from application.common.models.money_dto import MoneyDto


@dataclass(frozen=True)
class OrderItemDto:
    product_id: UUID
    quantity: int
    unit_price: MoneyDto
    product_name: str
