from sqlalchemy import Engine

from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.token_service import ITokenService
from infrastructure.data.application_db_context import ApplicationDbContext
from infrastructure.data.application_db_context_initialiser import initialise_demo
from infrastructure.data.connection import create_database_engine, create_session_factory
from infrastructure.identity.identity_service import IdentityService
from infrastructure.identity.password_hasher import PasswordHasher
from infrastructure.identity.token_service import TokenService
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway


def create_token_service(engine: Engine) -> ITokenService:
    return TokenService(create_session_factory(engine))


def create_identity_service(engine: Engine) -> IIdentityService:
    """Build the identity port; the host initialises the schema before calling this."""
    return IdentityService(create_session_factory(engine), PasswordHasher())


def create_demo_dependencies(database_url: str | None = None):
    engine = create_database_engine(database_url)
    initialise_demo(engine)
    sessions = create_session_factory(engine)
    return engine, lambda: ApplicationDbContext(sessions), FakePaymentGateway()
