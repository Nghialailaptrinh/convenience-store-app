from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.dependency_injection import create_sender
from application.identity.queries.get_current_user.get_current_user import GetCurrentUserQuery


def test_current_user_uses_authenticated_identity_not_request_id():
    identity = Mock()
    identity.get_user_name.return_value = "a@example.com"
    sender = create_sender(Mock(), Mock(), identity, current_user=SimpleNamespace(user_id="user-a"))
    result = sender.send(GetCurrentUserQuery())
    assert (result.user_id, result.email) == ("user-a", "a@example.com")
    identity.get_user_name.assert_called_once_with("user-a")
    identity.create_user.assert_not_called()


@pytest.mark.parametrize("user_id", [None, "deleted-user"])
def test_missing_or_deleted_user_is_unauthenticated(user_id):
    identity = Mock()
    identity.get_user_name.return_value = None
    sender = create_sender(Mock(), Mock(), identity, current_user=SimpleNamespace(user_id=user_id))
    with pytest.raises(UnauthenticatedError):
        sender.send(GetCurrentUserQuery())
