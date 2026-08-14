# WASMBOX

WASMBOX is a simplified browser/code execution platform designed to accept Python code from a user, process it through a FastAPI backend, and prepare it for a future WebAssembly execution environment.

## Architecture Overview

User Code
↓
FastAPI Backend
↓
Execution Service
↓
Future WASM Layer
↓
Result

## Current Implementation Status

The Part 1 foundation is now in place and includes:

- FastAPI backend foundation
- health check
- code submission endpoint
- Pydantic validation
- execution service abstraction
- stdout/error capture
- automated tests

This implementation is intentionally a development/demo execution layer. It is not a secure sandbox and should not be treated as production-grade isolation. The real sandboxing and security model will be implemented later with the WASM execution layer.

## Completed in Part 1

- FastAPI backend foundation
- health check
- code submission endpoint
- Pydantic validation
- structured JSON responses
- execution service abstraction
- stdout/error capture
- automated tests

## Planned Next

- real WASM execution integration
- stronger isolation/security model
- frontend implementation
- backend/frontend integration

## Setup

From the repository root:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API:

```bash
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
  "error": null
}
```

## Security Note

The current execution service is intended for local development and demonstration. It captures stdout and exceptions, but it is not a fully isolated sandbox. A later WASM-based execution layer will provide a more secure execution architecture.
