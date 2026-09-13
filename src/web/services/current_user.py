from dataclasses import dataclass

from application.common.interfaces.current_user import ICurrentUser


@dataclass(frozen=True)
class CurrentUser(ICurrentUser):
    """Request-scoped identity, populated only after HTTP authentication."""

    _user_id: str | None

    @property
    def user_id(self) -> str | None:
        return self._user_id

    @property
    def id(self) -> str | None:
        """Compatibility with the template's existing User protocol."""
        return self.user_id
