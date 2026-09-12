"""Enforce inward dependencies without importing frameworks."""
import ast
from pathlib import Path


def test_dependency_boundaries():
    root = Path(__file__).resolve().parents[2] / "src"
    forbidden = {
        "domain": {"application", "infrastructure", "web", "fastapi", "pydantic", "sqlalchemy"},
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
                    assert module.split(".")[0] not in denied, (path, module)
