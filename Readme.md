# WASMBOX

WASMBOX is a lightweight prototype for executing restricted Python snippets through a FastAPI backend and a Pyodide/WebAssembly execution bridge.

## Architecture Overview

Frontend
↓
FastAPI
↓
Validation Layer
↓
Node.js Bridge
↓
Pyodide / WebAssembly
↓
Structured Response

## Current Implementation Status

The project now includes:

- FastAPI backend foundation
- health check endpoint
- code execution endpoint
- request validation
- basic Python code validation
- Node.js bridge to Pyodide
- output and error capture
- execution metadata
- automated pytest coverage

<<<<<<< HEAD
<<<<<<< HEAD
Initial setup in progress.

- Tested the latest WASMBOX prototype and reviewed the current implementation. Verified the project structure and noted that the integrated prototype is functioning successfully.
=======
This implementation is intentionally a development/demo execution layer. It is not a secure sandbox and should not be treated as production-grade isolation. The real sandboxing and security model will be implemented later with the WASM execution layer.
=======
## Current Security Model
>>>>>>> 60d127b (tested WASMBOX prototype with Pyodide runtime and developer portal)

This is an educational/demo prototype. The system does not directly run submitted Python code on the host using `exec()`. Instead, the project delegates execution to a Node.js subprocess that initializes Pyodide in WebAssembly. Before execution, the backend validates code against a small blocked-pattern list and enforces a timeout and maximum length.

This is not a production-grade sandbox and should not be treated as complete isolation for arbitrary Python code.

## Supported Approach

- basic arithmetic statements
- integer variables
- print() output
- simple Python snippets in a controlled environment
- structured execution feedback

## Blocked Patterns

The validation layer rejects patterns such as:

- imports like `os`, `subprocess`, `socket`, `ctypes`, etc.
- builtins such as `eval`, `exec`, `compile`, `open`, `__import__`
- unsupported demo-only constructs such as function definitions, loops, and attribute access

## Setup

From the repository root:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cd wasm
npm install
```

Run the backend:

```bash
cd ..
uvicorn backend.app.main:app --reload
```

The API documentation is available at:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Example API Request

```http
POST /api/execute
Content-Type: application/json

{
  "code": "print('Hello WASMBOX')"
}
```

## Example API Response

```json
{
  "success": true,
  "output": "Hello WASMBOX\n",
  "error": null,
  "execution_time_ms": 42,
  "stage": "completed"
}
```

## Phase Evolution

<<<<<<< HEAD
The current execution service is intended for local development and demonstration. It captures stdout and exceptions, but it is not a fully isolated sandbox. A later WASM-based execution layer will provide a more secure execution architecture.
>>>>>>> 90b72aa (feat: add FastAPI code execution backend foundation)
=======
- Phase 1: FastAPI backend foundation and demo runtime scaffolding
- Phase 2A: Pyodide/WebAssembly execution bridge in Node.js
- Phase 2B: validation, timeout handling, metadata, and safer demo execution flow
>>>>>>> 60d127b (tested WASMBOX prototype with Pyodide runtime and developer portal)
