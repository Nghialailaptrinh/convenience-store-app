from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import pytest

from application.common.exceptions.invalid_credentials import InvalidCredentialsError
from application.common.exceptions.validation_exception import ValidationException
from application.common.models.authentication_result import AuthenticationResult
from application.dependency_injection import create_sender
from application.identity.commands.login_user.login_user import LoginUserCommand


def test_login_issues_token_only_after_valid_credentials():
    identity = Mock()
    tokens = Mock()
    identity.verify_credentials.return_value = "user-1"
    tokens.issue.return_value = AuthenticationResult("user-1", "secret-token", 3600)
    command = LoginUserCommand(" STUDENT@Example.com ", " password with spaces ")
    result = create_sender(Mock(), Mock(), identity, tokens).send(command)
    assert result.user_id == "user-1"
    assert result.access_token == "secret-token"
    assert "secret-token" not in repr(result)
    tokens.issue.assert_called_once_with("user-1")
    identity.verify_credentials.assert_called_once_with(
        "student@example.com", " password with spaces "
    )
    identity.create_user.assert_not_called()
    assert command.password not in repr(command)
    with pytest.raises(FrozenInstanceError):
        command.email = "changed@example.com"


def test_bad_credentials_raise_generic_error():
    identity = Mock()
    tokens = Mock()
    identity.verify_credentials.return_value = None
    with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
        create_sender(Mock(), Mock(), identity, tokens).send(
            LoginUserCommand("a@example.com", "wrong")
        )

    tokens.issue.assert_not_called()


@pytest.mark.parametrize(
    "email,password",
    [(" ", "password"), (None, "password"), ("a@example.com", ""), ("a@example.com", "x" * 129)],
)
def test_invalid_login_never_calls_identity(email, password):
    identity = Mock()
    tokens = Mock()
    with pytest.raises(ValidationException):
        create_sender(Mock(), Mock(), identity, tokens).send(LoginUserCommand(email, password))
    identity.verify_credentials.assert_not_called()
    tokens.issue.assert_not_called()
