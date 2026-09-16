from typing import Protocol

from application.common.models.result import Result


class IIdentityService(Protocol):
    """Account storage and credential checking; no HTTP or token dependency.

    create_user persists one transaction and returns (result, user_id).
    Read operations never persist changes.
    """

    def create_user(
        self, email: str, password: str, name: str | None = None
    ) -> tuple[Result, str | None]: ...
    def verify_credentials(self, email: str, password: str) -> str | None: ...
    def get_user_name(self, user_id: str) -> str | None: ...
    def get_display_name(self, user_id: str) -> str | None: ...
    def is_in_role(self, user_id: str, role: str) -> bool: ...


# Preserve the existing import name while following the project's I* port convention.
IdentityService = IIdentityService
