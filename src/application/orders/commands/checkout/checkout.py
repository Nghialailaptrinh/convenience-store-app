from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.payment_gateway import IPaymentGateway
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.security.require_customer import require_customer
from application.orders.common.build_order import build_order


@dataclass(frozen=True)
class CheckoutCommand(Request[UUID]):
    pass


class CheckoutCommandHandler(RequestHandler[CheckoutCommand, UUID]):
    def __init__(
        self,
        context: IApplicationDbContext,
        payment: IPaymentGateway,
        current_user: ICurrentUser | None,
    ) -> None:
        self._context = context
        self._current_user = current_user
        self._payment = payment

    def handle(self, request: CheckoutCommand) -> UUID:
        with self._context:
            customer_id = require_customer(self._context, self._current_user)
            order = build_order(customer_id, self._context)
            reference = self._payment.charge(customer_id, order.total)
            order.mark_paid(reference)
            self._context.orders.save(order)
            self._context.save_changes()
            return order.id
