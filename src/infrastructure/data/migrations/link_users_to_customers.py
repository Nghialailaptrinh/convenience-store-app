"""Additive, repeatable upgrade for existing local demo databases; never claim guest data."""

from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import Engine, inspect, select, text

from infrastructure.data.configurations.customer_configuration import CustomerRecord
from infrastructure.data.configurations.user_configuration import UserRecord


def link_users_to_customers(engine: Engine) -> None:
    with engine.begin() as connection:
        columns = {column["name"] for column in inspect(connection).get_columns("customers")}
        if "user_id" not in columns:
            connection.execute(
                text("ALTER TABLE customers ADD COLUMN user_id VARCHAR(36) REFERENCES users(id)")
            )
        connection.execute(
            text("CREATE UNIQUE INDEX IF NOT EXISTS ix_customers_user_id ON customers (user_id)")
        )
        existing = set(connection.execute(select(CustomerRecord.user_id)).scalars())
        for user in connection.execute(select(UserRecord.id, UserRecord.email)):
            if user.id not in existing:
                connection.execute(
                    CustomerRecord.__table__.insert().values(
                        id=str(uuid5(NAMESPACE_URL, f"shop:customer:user:{user.id}")),
                        name=user.email,
                        email=user.email,
                        user_id=user.id,
                    )
                )
