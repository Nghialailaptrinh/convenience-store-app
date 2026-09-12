from dataclasses import dataclass
from uuid import UUID

from application.carts.queries.get_cart.cart_item_dto import CartItemDto
from domain.entities.cart import Cart


@dataclass(frozen=True)
class CartDto:
    id: UUID
    customer_id: UUID
    items: list[CartItemDto]

    @classmethod
    def from_domain(cls, cart: Cart) -> "CartDto":
        return cls(
            cart.id, cart.customer_id, [CartItemDto(i.product_id, i.quantity) for i in cart.items]
        )
