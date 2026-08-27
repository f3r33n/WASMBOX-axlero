# WASMBOX ()

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

## Current Security Model 

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

## Setup  guide

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

- Phase 1: FastAPI backend foundation and demo runtime scaffolding
- Phase 2A: Pyodide/WebAssembly execution bridge in Node.js
- Phase 2B: validation, timeout handling, metadata, and safer demo execution flow

- Tested the WASMBOX prototype with the Pyodide runtime and developer portal. Verified that the frontend loads successfully and the backend connection is active.
