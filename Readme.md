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
## Current Security Model

This is an educational/demo prototype. Submitted Python code is not executed directly on the host; the backend delegates execution to a Node.js subprocess that initializes Pyodide in WebAssembly. Before execution, the backend validates code against a blocked-pattern list and enforces simple runtime limits (timeout and maximum code length).

This is not a production-grade sandbox and should not be treated as complete isolation for arbitrary Python code.

## Supported Approach (Demo)

- basic arithmetic and expression evaluation
- integer and simple variable usage
- `print()` output
- function definitions, `if`/`else`, `for` and `while` loops (controlled)
- list literals and basic list indexing
- simple comparisons used in conditional logic
- structured execution feedback from the Pyodide worker

## Blocked Patterns and Dangerous Operations

The validation layer rejects clearly risky or host-access patterns such as:

- imports (no external module imports are allowed)
- blocked modules: `os`, `sys`, `subprocess`, `socket`, `pathlib`, `shutil`, `ctypes`, `multiprocessing`
- builtins such as `eval`, `exec`, `compile`, `open`, and `__import__`
- attribute access (e.g. `obj.attr`) to avoid reaching host or runtime internals
- async functions, class definitions, lambdas, async loops, and context managers

The intent is to allow common Python learning constructs (functions, loops, lists, indexing, comparisons) while preventing filesystem, process, and attribute-level access to the runtime.

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

API docs:

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
- Phase 2B: validation, timeout handling, execution metadata, and safer demo execution flow
