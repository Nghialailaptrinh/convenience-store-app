from dataclasses import dataclass, field

from application.common.exceptions.invalid_credentials import InvalidCredentialsError
from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.common.interfaces.token_service import ITokenService
from application.common.models.authentication_result import AuthenticationResult


@dataclass(frozen=True)
class LoginUserCommand(Request[AuthenticationResult]):
    email: str
    password: str = field(repr=False)


class LoginUserCommandHandler(RequestHandler[LoginUserCommand, AuthenticationResult]):
    def __init__(self, identity: IIdentityService, tokens: ITokenService) -> None:
        self._identity = identity
        self._tokens = tokens

    def handle(self, request: LoginUserCommand) -> AuthenticationResult:
        user_id = self._identity.verify_credentials(
            request.email.strip().casefold(), request.password
        )
        if user_id is None:
            raise InvalidCredentialsError()
        return self._tokens.issue(user_id)
