from dataclasses import dataclass
from uuid import UUID

from domain.entities.cart_item import CartItem
from domain.value_objects.money import Money


@dataclass(frozen=True)
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: Money
    product_name: str = ""

    def __post_init__(self) -> None:
        CartItem.validate_quantity(self.quantity)
