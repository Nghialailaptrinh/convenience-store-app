from uuid import UUID

from sqlalchemy.orm import Session

from application.common.interfaces.order_repository import OrderRepository
from domain.entities.order import Order


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, order_id: UUID) -> Order | None:
        raise NotImplementedError("TODO: map database rows to order")

    def save(self, order: Order) -> None:
        raise NotImplementedError("TODO: persist order; transaction owned by caller")
