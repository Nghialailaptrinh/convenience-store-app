from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.payment_gateway import PaymentGateway
from application.common.interfaces.unit_of_work import UnitOfWork
from application.orders.commands.create_order.command import build_order


@dataclass(frozen=True)
class CheckoutCommand:
    customer_id: UUID


def handle(command: CheckoutCommand, uow: UnitOfWork, payment: PaymentGateway) -> UUID:
    with uow:
        order = build_order(command.customer_id, uow)
        reference = payment.charge(command.customer_id, order.total)
        order.mark_paid(reference)
        uow.orders.save(order)
        uow.commit()
        return order.id
