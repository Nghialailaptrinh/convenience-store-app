from infrastructure.data.application_db_context import ApplicationDbContext
from infrastructure.data.application_db_context_initialiser import initialise_demo
from infrastructure.data.connection import create_database_engine, create_session_factory
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway


def create_demo_dependencies(database_url: str | None = None):
    engine = create_database_engine(database_url)
    initialise_demo(engine)
    sessions = create_session_factory(engine)
    return engine, lambda: ApplicationDbContext(sessions), FakePaymentGateway()
