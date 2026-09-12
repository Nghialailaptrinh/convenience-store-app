from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.common.interfaces.cart_repository import CartRepository
from domain.entities.cart import Cart
from domain.entities.cart_item import CartItem
from infrastructure.data.models import CartRecord


class SqlAlchemyCartRepository(CartRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_customer_id(self, customer_id: UUID) -> Cart | None:
        row = self.session.scalar(select(CartRecord).where(
            CartRecord.customer_id == str(customer_id)))
        if row is None:
            return None
        return Cart(UUID(row.id), UUID(row.customer_id), [
            CartItem(UUID(item["product_id"]), item["quantity"]) for item in row.items])

    def save(self, cart: Cart) -> None:
        self.session.merge(CartRecord(id=str(cart.id), customer_id=str(cart.customer_id), items=[
            {"product_id": str(item.product_id), "quantity": item.quantity} for item in cart.items]))
