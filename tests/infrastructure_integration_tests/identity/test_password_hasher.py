import pytest

from infrastructure.identity.application_user import ApplicationUser
from infrastructure.identity.password_hasher import PasswordHasher


def test_password_hash_is_salted_and_verifies_unicode_without_trimming():
    hasher = PasswordHasher()
    password = "  a long password with \u0111 and \U0001f512  "
    first, second = hasher.hash(password), hasher.hash(password)
    assert first != second
    assert password not in first
    assert hasher.verify(password, first)
    assert not hasher.verify(password.strip(), first)
    assert not hasher.verify("incorrect password", first)
    assert first not in repr(ApplicationUser("id", "user@example.com", first))


@pytest.mark.parametrize(
    "encoded",
    [
        "corrupted",
        "scrypt$131072$8$1$zz$zz",
        "scrypt$131072$8$1$00$00",
        "scrypt$999999999$8$1$00$00",
    ],
)
def test_invalid_or_unsupported_hash_fails_closed(encoded):
    assert not PasswordHasher().verify("a long password", encoded)
