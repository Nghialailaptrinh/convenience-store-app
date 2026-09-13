from dataclasses import dataclass

from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.identity.queries.get_current_user.current_user_dto import CurrentUserDto


@dataclass(frozen=True)
class GetCurrentUserQuery(Request[CurrentUserDto]):
    pass


class GetCurrentUserQueryHandler(RequestHandler[GetCurrentUserQuery, CurrentUserDto]):
    def __init__(self, current_user: ICurrentUser, identity: IIdentityService) -> None:
        self._current_user = current_user
        self._identity = identity

    def handle(self, request: GetCurrentUserQuery) -> CurrentUserDto:
        user_id = self._current_user.user_id
        if user_id is None:
            raise UnauthenticatedError()
        email = self._identity.get_user_name(user_id)
        if email is None:
            raise UnauthenticatedError()
        return CurrentUserDto(user_id, email)
