"""Focused validation tests for the WASMBOX demo environment."""

from fastapi.testclient import TestClient

from backend.app.config import MAX_CODE_LENGTH
from backend.app.main import app
from backend.app.services.validator import validate_python_code

client = TestClient(app)


def test_blocked_import_is_rejected() -> None:
    """Importing os should be blocked by the validation layer."""
    response = client.post("/api/execute", json={"code": "import os"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["stage"] == "validation"
    assert "os" in data["error"]


def test_blocked_eval_is_rejected() -> None:
    """Builtins such as eval should be banned in the prototype environment."""
    response = client.post("/api/execute", json={"code": "eval('1 + 1')"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["stage"] == "validation"
    assert "eval" in data["error"]


def test_overlong_code_is_rejected() -> None:
    """Code longer than the configured maximum should fail before worker execution."""
    response = client.post("/api/execute", json={"code": "x = 1\n" * (MAX_CODE_LENGTH + 1)})
    assert response.status_code == 422


def test_function_definition_allowed() -> None:
    """Normal Python function definitions should be allowed."""
    validate_python_code(
        """
def hello():
    print("Hello")

hello()
"""
    )


def test_for_loop_allowed() -> None:
    """Normal Python for loops should be allowed."""
    validate_python_code(
        """
for i in range(3):
    print(i)
"""
    )


def test_list_literals_allowed() -> None:
    """Normal Python list literals should be allowed."""
    validate_python_code(
        """
numbers = [1, 2, 3]
print(numbers)
"""
    )


def test_list_indexing_allowed() -> None:
    """Basic list indexing should be allowed."""
    validate_python_code(
        """
numbers = [10, 20, 30]
print(numbers[0])
"""
    )
