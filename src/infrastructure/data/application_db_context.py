from sqlalchemy.orm import Session, sessionmaker

from application.common.interfaces.application_db_context import IApplicationDbContext
from infrastructure.repositories.sqlalchemy_cart_repository import (
    SqlAlchemyCartRepository,
)
from infrastructure.repositories.sqlalchemy_customer_repository import SqlAlchemyCustomerRepository
from infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)
from infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)


class ApplicationDbContext(IApplicationDbContext):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        try:
            # Serialize this small SQLite demo to prevent lost cart updates/double checkout.
            # Reads use the same transaction boundary but never persist changes.
            if self.session.bind.dialect.name == "sqlite":
                self.session.connection().exec_driver_sql("BEGIN IMMEDIATE")
            self.customers = SqlAlchemyCustomerRepository(self.session)
            self.products = SqlAlchemyProductRepository(self.session)
            self.carts = SqlAlchemyCartRepository(self.session)
            self.orders = SqlAlchemyOrderRepository(self.session)
            return self
        except Exception:
            self.session.close()
            raise

    def save_changes(self) -> None:
        self.session.commit()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            self.session.rollback()
        finally:
            self.session.close()
