from uuid import UUID, uuid4

from application.common.interfaces.payment_gateway import IPaymentGateway
from application.common.exceptions.payment_failed import PaymentFailedError
from domain.value_objects.money import Money


class FakePaymentGateway(IPaymentGateway):
    """Demo only: no external calls, no actual money movement."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def charge(self, customer_id: UUID, amount: Money) -> str:
        if self.fail:
            raise PaymentFailedError("Demo payment declined; cart has been preserved")
        return f"demo-{uuid4()}"
