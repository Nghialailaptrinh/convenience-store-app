import re
import secrets
from uuid import NAMESPACE_URL, uuid4, uuid5

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from application.common.interfaces.identity_service import IIdentityService
from application.common.models.result import Result
from infrastructure.data.configurations.customer_configuration import CustomerRecord
from infrastructure.data.configurations.user_configuration import UserRecord
from infrastructure.identity.application_user import ApplicationUser
from infrastructure.identity.password_hasher import PasswordHasher


class IdentityService(IIdentityService):
    def __init__(self, sessions: sessionmaker[Session], password_hasher: PasswordHasher) -> None:
        self._sessions = sessions
        self._password_hasher = password_hasher
        # Unknown emails still perform password hashing before returning a failed check.
        self._dummy_hash = password_hasher.hash(secrets.token_urlsafe(32))

    def create_user(
        self, email: str, password: str, name: str | None = None
    ) -> tuple[Result, str | None]:
        if name is not None and (not isinstance(name, str) or not 1 <= len(name.strip()) <= 100):
            return Result(False, ("Name must contain 1 to 100 characters",)), None
        email = email.strip().casefold()
        if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            return Result(False, ("Enter a valid email address",)), None
        if not 15 <= len(password) <= 128:
            return Result(False, ("Password must contain 15 to 128 characters",)), None
        user = ApplicationUser(str(uuid4()), email, self._password_hasher.hash(password))
        try:
            with self._sessions.begin() as session:
                session.add(
                    UserRecord(id=user.id, email=user.email, password_hash=user.password_hash)
                )
                session.flush()
                session.add(
                    CustomerRecord(
                        id=str(uuid5(NAMESPACE_URL, f"shop:customer:user:{user.id}")),
                        name=name.strip() if name is not None else user.email,
                        email=user.email,
                        user_id=user.id,
                    )
                )
        except IntegrityError:
            # The unique constraint also protects concurrent account creation.
            with self._sessions() as session:
                exists = session.scalar(select(UserRecord.id).where(UserRecord.email == email))
            if exists is not None:
                return Result(False, ("An account with this email already exists",)), None
            raise
        return Result(True), user.id

    def verify_credentials(self, email: str, password: str) -> str | None:
        if len(email) > 254 or not 1 <= len(password) <= 128:
            return None
        with self._sessions() as session:
            user = session.scalar(
                select(UserRecord).where(UserRecord.email == email.strip().casefold())
            )
            encoded = user.password_hash if user else self._dummy_hash
            valid = self._password_hasher.verify(password, encoded)
            return user.id if user is not None and valid else None

    def get_user_name(self, user_id: str) -> str | None:
        # Email remains the login name; Customer.name is the separate display name.
        with self._sessions() as session:
            user = session.get(UserRecord, user_id)
            return user.email if user else None

    def get_display_name(self, user_id: str) -> str | None:
        with self._sessions() as session:
            return session.scalar(
                select(CustomerRecord.name).where(CustomerRecord.user_id == user_id)
            )

    def is_in_role(self, user_id: str, role: str) -> bool:
        raise NotImplementedError("Role authorization is not configured")
