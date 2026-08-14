"""Execution service for the development/demo backend layer.

The current execution implementation is intentionally simple and is intended for
local development and demonstration only. It captures stdout and Python runtime
exceptions and returns them in a structured response. The planned WASM layer will
later provide a more isolated execution architecture, but the FastAPI API should
remain stable while that environment is introduced.
"""

from __future__ import annotations

import io
import traceback
from contextlib import redirect_stdout
from typing import Any

from backend.app.models import CodeExecutionResponse


def execute_python_code(source_code: str) -> CodeExecutionResponse:
    """Execute submitted Python source code in a controlled local demo environment.

    This is not a production-grade sandbox. It is a development/demo execution
    layer that is easier to replace later with a WASM-based runtime.
    """
    buffer = io.StringIO()

    try:
        with redirect_stdout(buffer):
            exec(compile(source_code, "<wasmbox-input>", "exec"), {"__builtins__": __builtins__})
        return CodeExecutionResponse(success=True, output=buffer.getvalue(), error=None)
    except Exception as exc:  # pragma: no cover - broad catch needed for execution behavior
        error_message = traceback.format_exc().strip() or str(exc)
        return CodeExecutionResponse(success=False, output="", error=error_message)
