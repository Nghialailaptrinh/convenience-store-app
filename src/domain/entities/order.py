from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.order_item import OrderItem
from domain.enums.order_status import OrderStatus


@dataclass
class Order:
    id: UUID
    customer_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    items: list[OrderItem] = field(default_factory=list)
