from application.common.exceptions.validation_exception import ValidationException
from application.identity.commands.login_user.login_user import LoginUserCommand


class LoginUserCommandValidator:
    def validate(self, request: LoginUserCommand) -> None:
        errors = {}
        if (
            not isinstance(request.email, str)
            or not 1 <= len(request.email.strip().casefold()) <= 254
        ):
            errors["email"] = ["Email is required (maximum 254 characters)"]
        if not isinstance(request.password, str) or not 1 <= len(request.password) <= 128:
            errors["password"] = ["Password is required (maximum 128 characters)"]
        if errors:
            raise ValidationException(errors)
