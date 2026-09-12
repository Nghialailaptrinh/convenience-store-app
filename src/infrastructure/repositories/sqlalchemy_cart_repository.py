from uuid import UUID

from sqlalchemy.orm import Session

from application.common.interfaces.cart_repository import CartRepository
from domain.entities.cart import Cart


class SqlAlchemyCartRepository(CartRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_customer_id(self, customer_id: UUID) -> Cart | None:
        raise NotImplementedError("TODO: map database rows to cart")

    def save(self, cart: Cart) -> None:
        raise NotImplementedError("TODO: persist cart; transaction owned by caller")
