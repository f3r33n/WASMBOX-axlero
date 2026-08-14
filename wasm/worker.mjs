import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

function safeJson(value) {
  return JSON.stringify(value);
}

async function loadPyodide() {
  const pyodideModule = await import('pyodide/pyodide.mjs');
  const pyodide = await pyodideModule.loadPyodide({
    indexURL: path.join(__dirname, 'node_modules', 'pyodide'),
  });
  return pyodide;
}

async function main() {
  try {
    const rawInput = await readStdin();
    const payload = rawInput.trim() ? JSON.parse(rawInput) : {};
    const code = typeof payload.code === 'string' ? payload.code : '';

    if (!code || !code.trim()) {
      process.stdout.write(
        safeJson({
          success: false,
          output: '',
          error: 'Code cannot be empty or whitespace only.',
        })
      );
      return;
    }

    const pyodide = await loadPyodide();

    let capturedOutput = '';
    let capturedError = null;

    pyodide.setStdout({
      batched: (text) => {
        capturedOutput += text;
      },
    });

    pyodide.setStderr({
      batched: (text) => {
        capturedError = (capturedError ?? '') + text;
      },
    });

    try {
      pyodide.runPython(code);
      process.stdout.write(
        safeJson({
          success: true,
          output: capturedOutput,
          error: null,
        })
      );
      return;
    } catch (err) {
      process.stdout.write(
        safeJson({
          success: false,
          output: capturedOutput,
          error: String(err instanceof Error ? err.message : err),
        })
      );
      return;
    }
  } catch (err) {
    process.stdout.write(
      safeJson({
        success: false,
        output: '',
        error: `Pyodide worker failure: ${err instanceof Error ? err.message : String(err)}`,
      })
    );
  }
}

main();
