from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import pytest

from application.common.exceptions.registration_failed import RegistrationFailedError
from application.common.exceptions.validation_exception import ValidationException
from application.common.models.result import Result
from application.dependency_injection import create_sender
from application.identity.commands.register_user.register_user import RegisterUserCommand

PASSWORD = "a sufficiently long password"


def test_register_dispatches_and_normalizes_email_without_changing_password():
    identity = Mock()
    identity.create_user.return_value = (Result(True), "user-1")
    sender = create_sender(Mock(), Mock(), identity)
    command = RegisterUserCommand(" STUDENT@Example.com ", PASSWORD)
    assert sender.send(command) == "user-1"
    identity.create_user.assert_called_once_with("student@example.com", PASSWORD, None)
    assert PASSWORD not in repr(command)
    with pytest.raises(FrozenInstanceError):
        command.email = "changed@example.com"


@pytest.mark.parametrize(
    "email,password",
    [
        ("invalid", PASSWORD),
        (None, PASSWORD),
        ("a@example.com", "short"),
        ("a@example.com", "x" * 129),
        ("a@example.com", None),
    ],
)
def test_invalid_register_never_calls_identity(email, password):
    identity = Mock()
    with pytest.raises(ValidationException):
        create_sender(Mock(), Mock(), identity).send(RegisterUserCommand(email, password))
    identity.create_user.assert_not_called()


def test_registration_failure_is_an_application_exception():
    identity = Mock()
    identity.create_user.return_value = (Result(False, ("Email already exists",)), None)
    with pytest.raises(RegistrationFailedError, match="Email already exists"):
        create_sender(Mock(), Mock(), identity).send(RegisterUserCommand("a@example.com", PASSWORD))
