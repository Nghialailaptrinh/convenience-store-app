from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.common.interfaces.order_repository import IOrderRepository
from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from domain.enums.order_status import OrderStatus
from domain.value_objects.money import Money
from infrastructure.data.configurations.order_configuration import OrderRecord


class SqlAlchemyOrderRepository(IOrderRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, order_id: UUID) -> Order | None:
        row = self.session.get(OrderRecord, str(order_id))
        if row is None:
            return None
        return self._to_domain(row)

    def get_by_customer_id(self, customer_id: UUID) -> list[Order]:
        rows = self.session.scalars(
            select(OrderRecord)
            .where(OrderRecord.customer_id == str(customer_id))
            .order_by(OrderRecord.id)
        )
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(row: OrderRecord) -> Order:
        return Order(
            id=UUID(row.id),
            customer_id=UUID(row.customer_id),
            status=OrderStatus(row.status),
            payment_reference=row.payment_reference,
            items=[
                OrderItem(
                    UUID(item["product_id"]),
                    item["quantity"],
                    Money(Decimal(item["amount"]), item["currency"]),
                    item["product_name"],
                )
                for item in row.items
            ],
        )

    def save(self, order: Order) -> None:
        self.session.merge(
            OrderRecord(
                id=str(order.id),
                customer_id=str(order.customer_id),
                status=order.status.value,
                payment_reference=order.payment_reference,
                items=[
                    {
                        "product_id": str(item.product_id),
                        "quantity": item.quantity,
                        "amount": str(item.unit_price.amount),
                        "currency": item.unit_price.currency,
                        "product_name": item.product_name,
                    }
                    for item in order.items
                ],
            )
        )
