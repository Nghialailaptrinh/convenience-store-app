import hashlib

from sqlalchemy import delete, event, select
from sqlalchemy.orm import Session

from infrastructure.data.configurations.access_token_configuration import AccessTokenRecord
from infrastructure.data.configurations.user_configuration import UserRecord
from infrastructure.data.connection import create_session_factory
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service
from infrastructure.identity.token_service import TokenService


def test_tokens_are_hashed_expire_and_validation_does_not_commit(tmp_path):
    engine, _, _ = create_demo_dependencies(f"sqlite:///{tmp_path / 'tokens.db'}")
    try:
        _, user_id = create_identity_service(engine).create_user(
            "a@example.com", "a sufficiently long password"
        )
        now = [1000]
        tokens = TokenService(create_session_factory(engine), 60, lambda: now[0])
        commits = []
        event.listen(engine, "commit", lambda connection: commits.append(True))
        first, second = tokens.issue(user_id), tokens.issue(user_id)
        assert first.access_token != second.access_token
        assert len(commits) == 2
        assert tokens.validate(first.access_token) == user_id
        with Session(engine) as session:
            stored = session.get(
                AccessTokenRecord, hashlib.sha256(first.access_token.encode()).hexdigest()
            )
            assert stored and stored.expires_at == 1060
            assert stored.token_hash != first.access_token
        now[0] = 1060
        assert tokens.validate(first.access_token) is None
        assert len(commits) == 2
        with Session(engine) as session:
            assert len(session.scalars(select(AccessTokenRecord)).all()) == 2
        tokens.issue(user_id)
        with Session(engine) as session:
            assert len(session.scalars(select(AccessTokenRecord)).all()) == 1
    finally:
        engine.dispose()


def test_token_for_deleted_user_is_invalid(tmp_path):
    engine, _, _ = create_demo_dependencies(f"sqlite:///{tmp_path / 'deleted.db'}")
    try:
        _, user_id = create_identity_service(engine).create_user(
            "a@example.com", "a sufficiently long password"
        )
        tokens = TokenService(create_session_factory(engine))
        token = tokens.issue(user_id).access_token
        with Session(engine) as session:
            # SQLite demo does not enable FK enforcement: orphaned tokens must still fail validation.
            session.execute(delete(UserRecord).where(UserRecord.id == user_id))
            session.commit()
        assert tokens.validate(token) is None
    finally:
        engine.dispose()
