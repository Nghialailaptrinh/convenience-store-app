from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.cart_item import CartItem
from domain.exceptions.business_rule_error import BusinessRuleError


@dataclass
class Cart:
    id: UUID
    customer_id: UUID
    items: list[CartItem] = field(default_factory=list)

    def add(self, product_id: UUID, quantity: int) -> None:
        CartItem.validate_quantity(quantity)
        item = next((item for item in self.items if item.product_id == product_id), None)
        if item is None:
            self.items.append(CartItem(product_id, quantity))
        else:
            self.update_quantity(product_id, item.quantity + quantity)

    def update_quantity(self, product_id: UUID, quantity: int) -> None:
        CartItem.validate_quantity(quantity)
        item = next((item for item in self.items if item.product_id == product_id), None)
        if item is None:
            raise BusinessRuleError("Sản phẩm không có trong giỏ hàng.")
        item.quantity = quantity

    def remove(self, product_id: UUID) -> None:
        self.items = [item for item in self.items if item.product_id != product_id]

    def clear(self) -> None:
        self.items.clear()
