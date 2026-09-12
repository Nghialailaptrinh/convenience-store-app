"""Keep future slices aligned with the agreed command/handler implementation pattern."""

import ast
from pathlib import Path


def test_slices_use_constructor_injected_handlers():
    root = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "pyproject.toml").is_file()
    )
    application = root / "src/application"
    slices = []
    for path in application.rglob("*.py"):
        if not {"commands", "queries"}.intersection(path.relative_to(application).parts):
            continue
        nodes = ast.parse(path.read_text(encoding="utf-8")).body
        requests = [
            node
            for node in nodes
            if isinstance(node, ast.ClassDef) and node.name.endswith(("Command", "Query"))
        ]
        if requests:
            slices.append((path, nodes, requests))
    assert slices
    for path, nodes, requests in slices:
        assert path.stem == path.parent.name, path
        assert not any(
            isinstance(node, ast.FunctionDef) and node.name == "handle" for node in nodes
        ), path
        assert len(requests) == 1, path
        request = requests[0]
        handlers = [
            node
            for node in nodes
            if isinstance(node, ast.ClassDef) and node.name == request.name + "Handler"
        ]
        assert len(handlers) == 1, path
        methods = {
            node.name: node for node in handlers[0].body if isinstance(node, ast.FunctionDef)
        }
        assert "__init__" in methods, path
        assert "handle" in methods, path
        assert [arg.arg for arg in methods["handle"].args.args] == ["self", "request"], path
