"""Tests for code execution behavior through the API."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_execute_success() -> None:
    """A valid code snippet should run and return its output."""
    response = client.post("/api/execute", json={"code": "print('Hello')"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Hello" in data["output"]
    assert data["error"] is None
    assert data["stage"] == "completed"
    assert isinstance(data["execution_time_ms"], (int, float))


def test_execute_empty_code_rejected() -> None:
    """Empty or whitespace-only code should be rejected by validation."""
    response = client.post("/api/execute", json={"code": "   "})
    assert response.status_code == 422


def test_execute_runtime_error_handled() -> None:
    """Runtime exceptions should be captured without crashing the API."""
    response = client.post("/api/execute", json={"code": "print(unknown_variable)"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["output"] == ""
    assert "unknown_variable" in data["error"]
    assert data["stage"] in {"runtime", "wasm"}
