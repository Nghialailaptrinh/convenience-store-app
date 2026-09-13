from typing import Protocol

from application.common.models.authentication_result import AuthenticationResult


class ITokenService(Protocol):
    def issue(self, user_id: str) -> AuthenticationResult:
        """Persist one token in one transaction after credentials have been verified."""
        ...

    def validate(self, token: str) -> str | None:
        """Read-only: return the user ID for an unexpired token, otherwise None."""
        ...
