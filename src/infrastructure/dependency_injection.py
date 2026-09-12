from infrastructure.data.connection import create_database_engine, create_session_factory
from infrastructure.data.initialiser import initialise_demo
from infrastructure.data.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway


def create_demo_dependencies(database_url: str | None = None):
    engine = create_database_engine(database_url)
    initialise_demo(engine)
    sessions = create_session_factory(engine)
    return engine, lambda: SqlAlchemyUnitOfWork(sessions), FakePaymentGateway()
