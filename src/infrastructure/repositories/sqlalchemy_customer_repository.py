from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.common.interfaces.customer_repository import ICustomerRepository
from domain.entities.customer import Customer
from infrastructure.data.configurations.customer_configuration import CustomerRecord


class SqlAlchemyCustomerRepository(ICustomerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_user_id(self, user_id: str) -> Customer | None:
        row = self._session.scalar(select(CustomerRecord).where(CustomerRecord.user_id == user_id))
        return Customer(UUID(row.id), row.name, row.email, row.user_id) if row else None
