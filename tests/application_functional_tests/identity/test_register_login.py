from sqlalchemy import event

from application.dependency_injection import create_sender
from application.identity.commands.login_user.login_user import LoginUserCommand
from application.identity.commands.register_user.register_user import RegisterUserCommand
from infrastructure.dependency_injection import (
    create_demo_dependencies,
    create_identity_service,
    create_token_service,
)


def test_register_and_login_each_save_one_transaction(tmp_path):
    engine, contexts, payment = create_demo_dependencies(f"sqlite:///{tmp_path / 'use_cases.db'}")
    try:
        sender = create_sender(
            contexts, payment, create_identity_service(engine), create_token_service(engine)
        )
        commits = []
        event.listen(engine, "commit", lambda connection: commits.append(True))
        password = "a sufficiently long password"
        user_id = sender.send(RegisterUserCommand("student@example.com", password))
        assert len(commits) == 1
        result = sender.send(LoginUserCommand("student@example.com", password))
        assert result.user_id == user_id
        assert len(commits) == 2
    finally:
        engine.dispose()
