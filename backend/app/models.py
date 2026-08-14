"""Pydantic models for incoming and outgoing execution payloads."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from backend.app.config import MAX_CODE_LENGTH


class CodeExecutionRequest(BaseModel):
    """Request payload for executing submitted Python code."""

    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        """Reject empty or whitespace-only code submissions."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Code cannot be empty or whitespace only.")
        if len(cleaned) > MAX_CODE_LENGTH:
            raise ValueError(f"Code must be {MAX_CODE_LENGTH} characters or fewer.")
        return cleaned


class CodeExecutionResponse(BaseModel):
    """Structured response returned after code execution."""

    success: bool
    output: str = ""
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    stage: str = "executed"
