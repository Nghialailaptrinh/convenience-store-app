from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from domain.entities.order_item import OrderItem
from domain.enums.order_status import OrderStatus
from domain.exceptions.business_rule_error import BusinessRuleError
from domain.value_objects.money import Money


@dataclass
class Order:
    id: UUID
    customer_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    items: list[OrderItem] = field(default_factory=list)
    payment_reference: str | None = None

    def __post_init__(self) -> None:
        if not self.items:
            raise BusinessRuleError("Không thể tạo đơn từ giỏ hàng trống.")

    @property
    def total(self) -> Money:
        return Money(sum((item.unit_price.amount * item.quantity for item in self.items), Decimal(0)))

    def mark_paid(self, reference: str) -> None:
        if self.status != OrderStatus.PENDING or not reference:
            raise BusinessRuleError("Chỉ đơn chờ thanh toán mới được thanh toán.")
        self.status = OrderStatus.PAID
        self.payment_reference = reference

    def cancel(self) -> None:
        if self.status == OrderStatus.CANCELLED:
            return
        if self.status != OrderStatus.PENDING:
            raise BusinessRuleError("Chỉ có thể hủy đơn chờ thanh toán.")
        self.status = OrderStatus.CANCELLED
