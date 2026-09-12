from uuid import UUID

from domain.value_objects.money import Money


class FakePaymentGateway:
    def charge(self, customer_id: UUID, amount: Money) -> str:
        raise NotImplementedError("Payment adapter is not configured; no payment was made")
