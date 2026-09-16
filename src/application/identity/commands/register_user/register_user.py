from dataclasses import dataclass, field

from application.common.exceptions.registration_failed import RegistrationFailedError
from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler


@dataclass(frozen=True)
class RegisterUserCommand(Request[str]):
    email: str
    password: str = field(repr=False)
    name: str | None = None


class RegisterUserCommandHandler(RequestHandler[RegisterUserCommand, str]):
    def __init__(self, identity: IIdentityService) -> None:
        self._identity = identity

    def handle(self, request: RegisterUserCommand) -> str:
        result, user_id = self._identity.create_user(
            request.email.strip().casefold(),
            request.password,
            request.name.strip() if request.name is not None else None,
        )
        if not result.succeeded:
            raise RegistrationFailedError("; ".join(result.errors) or "Registration failed")
        if user_id is None:
            raise RuntimeError("Identity provider returned success without a user ID")
        return user_id
