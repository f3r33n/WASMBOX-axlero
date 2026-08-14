"""FastAPI application entry point for the WASMBOX backend."""

from __future__ import annotations

from fastapi import FastAPI

from backend.app.config import APP_NAME, APP_VERSION
from backend.app.routers.code import router as code_router

app = FastAPI(
    title="WASMBOX API",
    version=APP_VERSION,
    description=(
        "A lightweight FastAPI backend for accepting Python code snippets, executing "
        "them in a development/demo environment, and returning structured results. "
        "The eventual production execution layer will be backed by WebAssembly."
    ),
)

app.include_router(code_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic API information."""
    return {
        "message": "Welcome to WASMBOX API",
        "status": "running",
        "version": APP_VERSION,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the current health status of the backend."""
    return {"status": "healthy"}
