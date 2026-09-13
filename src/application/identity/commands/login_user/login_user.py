from dataclasses import dataclass, field

from application.common.exceptions.invalid_credentials import InvalidCredentialsError
from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.models.authentication_result import AuthenticationResult


@dataclass(frozen=True)
class LoginUserCommand(Request[AuthenticationResult]):
    email: str
    password: str = field(repr=False)


class LoginUserCommandHandler(RequestHandler[LoginUserCommand, AuthenticationResult]):
    def __init__(self, identity: IIdentityService) -> None:
        self._identity = identity

    def handle(self, request: LoginUserCommand) -> AuthenticationResult:
        user_id = self._identity.verify_credentials(
            request.email.strip().casefold(), request.password
        )
        if user_id is None:
            raise InvalidCredentialsError()
        return AuthenticationResult(user_id)
