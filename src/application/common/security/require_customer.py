from uuid import UUID

from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser


def require_customer(context: IApplicationDbContext, current_user: ICurrentUser | None) -> UUID:
    """Resolve ownership inside Application, never from client-supplied customer IDs."""
    if current_user is None or current_user.user_id is None:
        raise UnauthenticatedError()
    customer = context.customers.get_by_user_id(current_user.user_id)
    if customer is None:
        raise UnauthenticatedError()
    return customer.id
