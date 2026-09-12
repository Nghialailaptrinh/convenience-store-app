from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.payment_gateway import PaymentGateway
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.orders.common.build_order import build_order


@dataclass(frozen=True)
class CheckoutCommand(Request[UUID]):
    customer_id: UUID


class CheckoutCommandHandler(RequestHandler[CheckoutCommand, UUID]):
    def __init__(self, context: ApplicationDbContext, payment: PaymentGateway) -> None:
        self._context = context
        self._payment = payment

    def handle(self, request: CheckoutCommand) -> UUID:
        with self._context:
            order = build_order(request.customer_id, self._context)
            reference = self._payment.charge(request.customer_id, order.total)
            order.mark_paid(reference)
            self._context.orders.save(order)
            self._context.save_changes()
            return order.id
