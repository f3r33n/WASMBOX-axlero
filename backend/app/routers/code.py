"""Routes used to submit and execute Python snippets."""

from __future__ import annotations

from fastapi import APIRouter

from backend.app.models import CodeExecutionRequest, CodeExecutionResponse
from backend.app.services.execution import execute_python_code

router = APIRouter(prefix="/api", tags=["execution"])


@router.post("/execute", response_model=CodeExecutionResponse)
def execute_code(payload: CodeExecutionRequest) -> CodeExecutionResponse:
    """Execute submitted Python source code via the development execution service."""
    return execute_python_code(payload.code)
