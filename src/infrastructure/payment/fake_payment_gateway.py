from uuid import UUID, uuid4

from src.domain.value_objects.money import Money


class FakePaymentGateway:
    def charge(self, customer_id: UUID, amount: Money) -> str:
        raise NotImplementedError("TODO: replace with a real payment provider")
