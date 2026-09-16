import sqlite3
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.data.configurations.customer_configuration import CustomerRecord
from infrastructure.dependency_injection import create_demo_dependencies, create_identity_service


def test_legacy_schema_backfill_is_repeatable_and_never_claims_guest_data(tmp_path):
    path = tmp_path / "legacy.db"
    user_id, guest_id, cart_id, order_id = [str(uuid4()) for _ in range(4)]
    with sqlite3.connect(path) as connection:
        connection.executescript("""
        CREATE TABLE users (id VARCHAR(36) PRIMARY KEY, email VARCHAR(254) UNIQUE NOT NULL, password_hash VARCHAR(256) NOT NULL);
        CREATE TABLE customers (id VARCHAR(36) PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL);
        CREATE TABLE carts (id VARCHAR(36) PRIMARY KEY, customer_id TEXT UNIQUE NOT NULL, items JSON NOT NULL);
        CREATE TABLE orders (id VARCHAR(36) PRIMARY KEY, customer_id TEXT NOT NULL, status TEXT NOT NULL, items JSON NOT NULL, payment_reference TEXT);
        """)
        connection.execute(
            "INSERT INTO users VALUES (?,?,?)", (user_id, "old@example.com", "existing-hash")
        )
        connection.execute(
            "INSERT INTO customers VALUES (?,?,?)", (guest_id, "Guest", "guest@example.com")
        )
        connection.execute("INSERT INTO carts VALUES (?,?,?)", (cart_id, guest_id, "[]"))
        connection.execute(
            "INSERT INTO orders VALUES (?,?,?,?,?)", (order_id, guest_id, "pending", "[]", None)
        )
    snapshots = []
    for _ in range(2):
        engine, _, _ = create_demo_dependencies(f"sqlite:///{path}")
        try:
            with Session(engine) as session:
                rows = session.scalars(select(CustomerRecord)).all()
                assert len(rows) == 2
                mapped = next(row for row in rows if row.user_id == user_id)
                assert mapped.id != guest_id and mapped.id != user_id
                assert session.get(CustomerRecord, guest_id).user_id is None
                snapshots.append(mapped.id)
            with engine.connect() as connection:
                assert (
                    connection.exec_driver_sql("SELECT customer_id FROM carts").scalar() == guest_id
                )
                assert (
                    connection.exec_driver_sql("SELECT customer_id FROM orders").scalar()
                    == guest_id
                )
                assert (
                    connection.exec_driver_sql("SELECT password_hash FROM users").scalar()
                    == "existing-hash"
                )
        finally:
            engine.dispose()
    assert snapshots[0] == snapshots[1]


def test_registration_creates_customer_atomically_and_duplicate_leaves_no_orphan(tmp_path):
    engine, _, _ = create_demo_dependencies(f"sqlite:///{tmp_path / 'register.db'}")
    try:
        identity = create_identity_service(engine)
        result, user_id = identity.create_user("new@example.com", "a sufficiently long password")
        assert result.succeeded
        assert not identity.create_user("NEW@example.com", "a sufficiently long password")[
            0
        ].succeeded
        with Session(engine) as session:
            customers = session.scalars(select(CustomerRecord)).all()
            assert len(customers) == 1
            assert customers[0].user_id == user_id
    finally:
        engine.dispose()
