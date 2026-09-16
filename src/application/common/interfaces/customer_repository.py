from typing import Protocol

from domain.entities.customer import Customer


class ICustomerRepository(Protocol):
    def get_by_user_id(self, user_id: str) -> Customer | None: ...
