"""Pyodide-backed WASM execution bridge.

This is a Phase 2A prototype that runs Python code inside a Node.js process using
Pyodide, which itself runs Python in WebAssembly. It is intentionally limited to
controlled execution and does not claim to be a production sandbox.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from backend.app.config import EXECUTION_TIMEOUT_SECONDS, NODE_EXECUTABLE, PYODIDE_WORKER_PATH


class WorkerExecutionError(RuntimeError):
    """Raised when the Pyodide worker cannot execute the submitted code."""


def execute_pyodide_code(code: str) -> dict[str, Any]:
    """Execute Python code in a Node.js + Pyodide worker and return structured data."""
    if not code or not code.strip():
        raise WorkerExecutionError("Code cannot be empty or whitespace only.")

    node_executable = shutil.which(NODE_EXECUTABLE) or NODE_EXECUTABLE
    if not node_executable:
        raise WorkerExecutionError("Node.js executable not found. Please install Node.js and ensure it is available on PATH.")

    worker_path = Path(PYODIDE_WORKER_PATH)
    if not worker_path.exists():
        raise WorkerExecutionError(f"Pyodide worker not found: {worker_path}")

    payload = json.dumps({"code": code})

    try:
        completed = subprocess.run(
            [node_executable, str(worker_path)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkerExecutionError(
            f"Execution exceeded the configured time limit of {EXECUTION_TIMEOUT_SECONDS} seconds."
        ) from exc

    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()

    if completed.returncode != 0:
        error_text = stderr or "Pyodide worker exited without a useful error message."
        raise WorkerExecutionError(error_text)

    if not stdout:
        raise WorkerExecutionError("Pyodide worker returned no output.")

    try:
        result = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise WorkerExecutionError(f"Malformed JSON from Pyodide worker: {stdout[:200]}") from exc

    if not isinstance(result, dict):
        raise WorkerExecutionError("Pyodide worker returned an unexpected payload format.")

    success = bool(result.get("success"))
    output = str(result.get("output", ""))
    error = result.get("error")

    return {
        "success": success,
        "output": output,
        "error": error if error is not None else None,
    }
