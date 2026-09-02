"""Application-level validation for submitted Python snippets.

This is intentionally lightweight and designed for a student demo project. It is
not a production security boundary and does not claim to be a complete sandbox.
"""

from __future__ import annotations

import ast

BLOCKED_IMPORTS = {
    "os",
    "sys",
    "subprocess",
    "socket",
    "pathlib",
    "shutil",
    "ctypes",
    "multiprocessing",
}

BLOCKED_BUILTINS = {"eval", "exec", "compile", "open", "__import__"}


class ValidationError(ValueError):
    """Raised when submitted code violates the demo validation policy."""


class RestrictedCodeValidator(ast.NodeVisitor):
    """Reject clearly unsafe or unsupported Python patterns for the demo runtime."""

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            module_name = alias.name.split(".")[0]
            if module_name in BLOCKED_IMPORTS:
                raise ValidationError(f"Import of '{module_name}' is not allowed in the WASMBOX demo environment.")
        # Disallow any imports in the demo environment
        raise ValidationError("Imports are not allowed in the WASMBOX demo environment.")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        module_name = node.module.split(".")[0] if node.module else ""
        if module_name in BLOCKED_IMPORTS:
            raise ValidationError(f"Import of '{module_name}' is not allowed in the WASMBOX demo environment.")
        raise ValidationError("Imports are not allowed in the WASMBOX demo environment.")

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        func = node.func
        # Block calls to dangerous builtins
        if isinstance(func, ast.Name) and func.id in BLOCKED_BUILTINS:
            raise ValidationError(f"Calling '{func.id}' is not allowed in the WASMBOX demo environment.")
        # Disallow attribute-call forms (e.g. obj.method()) to prevent reaching into runtime
        if isinstance(func, ast.Attribute):
            raise ValidationError("Attribute access is not allowed in the WASMBOX demo environment.")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        raise ValidationError("Attribute access is not allowed in the WASMBOX demo environment.")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        # Allow function definitions but validate their bodies
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        raise ValidationError("Async functions are not allowed in the WASMBOX demo environment.")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        raise ValidationError("Class definitions are not allowed in the WASMBOX demo environment.")

    def visit_Lambda(self, node: ast.Lambda) -> None:  # noqa: N802
        raise ValidationError("Lambda expressions are not allowed in the WASMBOX demo environment.")

    def visit_For(self, node: ast.For) -> None:  # noqa: N802
        # Allow for-loops and validate their bodies
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:  # noqa: N802
        # Allow while-loops and validate their bodies
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:  # noqa: N802
        raise ValidationError("Async loops are not allowed in the WASMBOX demo environment.")

    def visit_With(self, node: ast.With) -> None:  # noqa: N802
        raise ValidationError("With statements are not allowed in the WASMBOX demo environment.")

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:  # noqa: N802
        raise ValidationError("Async context managers are not allowed in the WASMBOX demo environment.")

    def visit_List(self, node: ast.List) -> None:  # noqa: N802
        # Allow list literals and validate their elements
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:  # noqa: N802
        raise ValidationError("Dictionary literals are not allowed in the WASMBOX demo environment.")

    def visit_Set(self, node: ast.Set) -> None:  # noqa: N802
        raise ValidationError("Set literals are not allowed in the WASMBOX demo environment.")

    def visit_Tuple(self, node: ast.Tuple) -> None:  # noqa: N802
        raise ValidationError("Tuple literals are not allowed in the WASMBOX demo environment.")

    def visit_Subscript(self, node: ast.Subscript) -> None:  # noqa: N802
        # Allow indexing/subscript operations on allowed sequences
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:  # noqa: N802
        """Allow basic comparison operators used by normal conditional logic."""
        allowed_operators = (
            ast.Lt,
            ast.LtE,
            ast.Gt,
            ast.GtE,
            ast.Eq,
            ast.NotEq,
        )

        for operator in node.ops:
            if not isinstance(operator, allowed_operators):
                raise ValidationError(
                    "This comparison operator is not allowed in the WASMBOX demo environment."
                )

        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        super().generic_visit(node)


def validate_python_code(source_code: str) -> None:
    """Validate that the submitted code falls within the supported demo subset."""
    if not source_code or not source_code.strip():
        raise ValidationError("Code cannot be empty or whitespace only.")

    try:
        tree = ast.parse(source_code, mode="exec")
    except SyntaxError as exc:
        raise ValidationError(f"Invalid Python syntax: {exc.msg}") from exc

    validator = RestrictedCodeValidator()
    validator.visit(tree)
