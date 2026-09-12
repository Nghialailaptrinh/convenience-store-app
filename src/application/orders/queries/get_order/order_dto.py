from dataclasses import dataclass
from uuid import UUID

from application.common.models.money_dto import MoneyDto
from application.orders.queries.get_order.order_item_dto import OrderItemDto
from domain.entities.order import Order


@dataclass(frozen=True)
class OrderDto:
    id: UUID
    customer_id: UUID
    status: str
    items: list[OrderItemDto]
    total: MoneyDto
    payment_reference: str | None

    @classmethod
    def from_domain(cls, order: Order) -> "OrderDto":
        return cls(
            order.id,
            order.customer_id,
            order.status.value,
            [
                OrderItemDto(
                    i.product_id, i.quantity, MoneyDto.from_domain(i.unit_price), i.product_name
                )
                for i in order.items
            ],
            MoneyDto.from_domain(order.total),
            order.payment_reference,
        )
