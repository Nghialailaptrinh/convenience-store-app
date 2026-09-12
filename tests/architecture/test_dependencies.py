"""Enforce inward dependencies without importing frameworks."""

import ast
from pathlib import Path


def test_dependency_boundaries():
    repository = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyproject.toml").is_file()
    )
    root = repository / "src"
    forbidden = {
        "domain": {
            "application",
            "infrastructure",
            "web",
            "fastapi",
            "pydantic",
            "sqlalchemy",
        },
        "application": {"infrastructure", "web", "fastapi", "pydantic", "sqlalchemy"},
        "infrastructure": {"web", "fastapi"},
        "web": {"domain", "infrastructure", "sqlalchemy"},
    }
    for layer, denied in forbidden.items():
        for path in (root / layer).rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [node.module or ""]
                else:
                    continue
                for module in modules:
                    if path == root / "web/program.py" and module in {
                        "infrastructure.dependency_injection",
                        "domain.exceptions.business_rule_error",
                    }:
                        continue  # Explicit host composition and HTTP error mapping only.
                    assert module.split(".")[0] not in denied, (path, module)


def test_application_slices_depend_on_context_not_repository_adapters():
    repository = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyproject.toml").is_file()
    )
    application = repository / "src/application"
    for path in application.rglob("*.py"):
        relative_parts = path.relative_to(application).parts
        if not {"commands", "queries"}.intersection(relative_parts):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert not (
                    node.module
                    and node.module.startswith("application.common.interfaces.")
                    and node.module.endswith("_repository")
                ), (path, node.module)
