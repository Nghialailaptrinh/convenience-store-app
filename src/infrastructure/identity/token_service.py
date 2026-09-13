import hashlib
import re
import secrets
import time
from collections.abc import Callable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, sessionmaker

from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.common.interfaces.token_service import ITokenService
from application.common.models.authentication_result import AuthenticationResult
from infrastructure.data.configurations.access_token_configuration import AccessTokenRecord
from infrastructure.data.configurations.user_configuration import UserRecord


class TokenService(ITokenService):
    def __init__(
        self,
        sessions: sessionmaker[Session],
        lifetime_seconds: int = 60,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if lifetime_seconds <= 0:
            raise ValueError("Token lifetime must be positive")
        self._sessions = sessions
        self._lifetime = lifetime_seconds
        self._clock = clock

    def issue(self, user_id: str) -> AuthenticationResult:
        token = secrets.token_urlsafe(32)
        now = int(self._clock())
        with self._sessions.begin() as session:
            if session.get(UserRecord, user_id) is None:
                raise UnauthenticatedError()
            session.execute(delete(AccessTokenRecord).where(AccessTokenRecord.expires_at <= now))
            session.add(
                AccessTokenRecord(
                    token_hash=self._digest(token),
                    user_id=user_id,
                    expires_at=now + self._lifetime,
                )
            )
        return AuthenticationResult(user_id, token, self._lifetime)

    def validate(self, token: str) -> str | None:
        if not re.fullmatch(r"[A-Za-z0-9_-]{43}", token):
            return None
        with self._sessions() as session:
            return session.scalar(
                select(AccessTokenRecord.user_id)
                .join(UserRecord, UserRecord.id == AccessTokenRecord.user_id)
                .where(
                    AccessTokenRecord.token_hash == self._digest(token),
                    AccessTokenRecord.expires_at > int(self._clock()),
                )
            )

    @staticmethod
    def _digest(token: str) -> str:
        return hashlib.sha256(token.encode("ascii")).hexdigest()
