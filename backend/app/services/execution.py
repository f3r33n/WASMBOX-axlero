"""Execution service for the WASMBOX backend.

This service invokes a controlled Node.js/Pyodide worker that runs Python within
WebAssembly. The implementation is intentionally simple and limited to a student
prototype; it is not a production sandbox or a general Python execution system.
"""

from __future__ import annotations

import time

from backend.app.config import MAX_CODE_LENGTH
from backend.app.models import CodeExecutionResponse
from backend.app.services.validator import ValidationError, validate_python_code
from backend.app.services.wasm_runtime import WorkerExecutionError, execute_pyodide_code


def execute_python_code(source_code: str) -> CodeExecutionResponse:
    """Validate, run, and return structured results for submitted Python code."""
    started_at = time.perf_counter()

    if not source_code or not source_code.strip():
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        return CodeExecutionResponse(
            success=False,
            output="",
            error="Code cannot be empty or whitespace only.",
            execution_time_ms=elapsed_ms,
            stage="validation",
        )

    if len(source_code.strip()) > MAX_CODE_LENGTH:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        return CodeExecutionResponse(
            success=False,
            output="",
            error=f"Code exceeds the allowed size limit of {MAX_CODE_LENGTH} characters.",
            execution_time_ms=elapsed_ms,
            stage="validation",
        )

    try:
        validate_python_code(source_code)
    except ValidationError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        return CodeExecutionResponse(
            success=False,
            output="",
            error=str(exc),
            execution_time_ms=elapsed_ms,
            stage="validation",
        )

    try:
        result = execute_pyodide_code(source_code)
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        return CodeExecutionResponse(
            success=result["success"],
            output=result["output"],
            error=result["error"],
            execution_time_ms=elapsed_ms,
            stage="completed" if result["success"] else "runtime",
        )
    except WorkerExecutionError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        message = str(exc)
        stage = "timeout" if "time limit" in message.lower() else "wasm"
        return CodeExecutionResponse(
            success=False,
            output="",
            error=message,
            execution_time_ms=elapsed_ms,
            stage=stage,
        )
