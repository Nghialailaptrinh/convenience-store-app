import re

from application.common.exceptions.validation_exception import ValidationException
from application.identity.commands.register_user.register_user import RegisterUserCommand


class RegisterUserCommandValidator:
    def validate(self, request: RegisterUserCommand) -> None:
        errors = {}
        if (
            not isinstance(request.email, str)
            or len(request.email.strip().casefold()) > 254
            or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", request.email.strip())
        ):
            errors["email"] = ["Enter a valid email address (maximum 254 characters)"]
        if not isinstance(request.password, str) or not 15 <= len(request.password) <= 128:
            errors["password"] = ["Password must contain 15 to 128 characters"]
        if request.name is not None and (
            not isinstance(request.name, str) or not 1 <= len(request.name.strip()) <= 100
        ):
            errors["name"] = ["Name must contain 1 to 100 characters"]
        if errors:
            raise ValidationException(errors)
