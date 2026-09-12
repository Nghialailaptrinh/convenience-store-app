from concurrent.futures import ThreadPoolExecutor
from uuid import UUID

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.orm import Session

from infrastructure.data.configurations.user_configuration import UserRecord
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service

PASSWORD = "a sufficiently long password"


@pytest.fixture
def identity(tmp_path):
    engine, _, _ = create_demo_dependencies(f"sqlite:///{tmp_path / 'identity.db'}")
    try:
        yield create_identity_service(engine), engine
    finally:
        engine.dispose()


def test_user_is_persisted_normalized_and_reads_do_not_commit(identity):
    service, engine = identity
    commits = []
    event.listen(engine, "commit", lambda connection: commits.append(True))
    result, user_id = service.create_user(" Student@Example.COM ", PASSWORD)
    assert result.succeeded and result.errors == ()
    assert UUID(user_id)
    assert len(commits) == 1
    assert service.get_user_name(user_id) == "student@example.com"
    assert service.get_user_name("missing") is None
    assert service.verify_credentials(" STUDENT@example.com ", PASSWORD) == user_id
    assert service.verify_credentials("student@example.com", "wrong password") is None
    assert service.verify_credentials("unknown@example.com", PASSWORD) is None
    assert len(commits) == 1
    with Session(engine) as session:
        record = session.get(UserRecord, user_id)
        assert record.password_hash != PASSWORD
        assert record.password_hash.startswith("scrypt$")
    assert (
        create_identity_service(engine).verify_credentials("student@example.com", PASSWORD)
        == user_id
    )


def test_duplicate_email_rolls_back_and_allows_later_registration(identity):
    service, engine = identity
    first, first_id = service.create_user("student@example.com", PASSWORD)
    duplicate, duplicate_id = service.create_user("STUDENT@example.com", PASSWORD)
    assert first.succeeded
    assert not duplicate.succeeded and duplicate.errors
    assert duplicate_id is None
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(UserRecord)) == 1
    assert service.verify_credentials("student@example.com", PASSWORD) == first_id
    assert service.create_user("another@example.com", PASSWORD)[0].succeeded


def test_concurrent_duplicate_email_creates_one_user(identity):
    service, engine = identity
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(lambda _: service.create_user("same@example.com", PASSWORD), range(2))
        )
    assert sum(result.succeeded for result, _ in results) == 1
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(UserRecord)) == 1


def test_invalid_credentials_are_rejected_before_persistence(identity):
    service, engine = identity
    for email, password in [
        ("invalid", PASSWORD),
        ("a@example.com", "short"),
        ("a@example.com", "x" * 129),
        ("", PASSWORD),
    ]:
        result, user_id = service.create_user(email, password)
        assert not result.succeeded and user_id is None
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(UserRecord)) == 0
    with pytest.raises(NotImplementedError, match="not configured"):
        service.is_in_role("some-user", "Admin")


def test_schema_initialization_preserves_users_and_shopping_data(tmp_path):
    database = f"sqlite:///{tmp_path / 'persist.db'}"
    engine, _, _ = create_demo_dependencies(database)
    try:
        identity = create_identity_service(engine)
        _, user_id = identity.create_user("student@example.com", PASSWORD)
        with engine.connect() as connection:
            products_before = connection.exec_driver_sql("SELECT * FROM products ORDER BY id").all()
            connection.exec_driver_sql(
                "INSERT INTO carts (id, customer_id, items) VALUES ('old-cart', 'old-customer', '[]')"
            )
            connection.commit()
    finally:
        engine.dispose()
    engine, _, _ = create_demo_dependencies(database)
    try:
        assert (
            create_identity_service(engine).verify_credentials("student@example.com", PASSWORD)
            == user_id
        )
        with engine.connect() as connection:
            assert (
                connection.exec_driver_sql("SELECT * FROM products ORDER BY id").all()
                == products_before
            )
            assert (
                connection.exec_driver_sql(
                    "SELECT customer_id FROM carts WHERE id = 'old-cart'"
                ).scalar()
                == "old-customer"
            )
    finally:
        engine.dispose()
