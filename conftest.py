"""Keep pytest temporary databases inside the project, isolated per invocation."""

from uuid import uuid4

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    # Respect an explicit --basetemp supplied by the caller.
    if config.option.basetemp is not None:
        return

    # A fresh path avoids sharing or deleting another pytest run's databases.
    # pytest creates the leaf directory when tmp_path is first requested.
    artifact_root = (config.rootpath / ".test_artifacts").resolve()
    if not artifact_root.is_relative_to(config.rootpath.resolve()):
        raise pytest.UsageError("Test artifacts must stay inside the project")
    artifact_root.mkdir(parents=True, exist_ok=True)
    config.option.basetemp = str(artifact_root / f"tmp-{uuid4().hex}")
