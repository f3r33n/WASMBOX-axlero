import { useCallback, useEffect, useMemo, useState } from 'react';
import './App.css';

const defaultCode = `print("Hello from WASMBOX")
for i in range(3):
    print(i)`;

const examples = {
  hello: {
    label: 'Hello World',
    code: `print("Hello from WASMBOX")`,
  },
  loop: {
    label: 'Loop',
    code: `for i in range(5):
    print("Iteration:", i)`,
  },
  arithmetic: {
    label: 'Arithmetic',
    code: `a = 12
b = 8
print("Sum:", a + b)
print("Product:", a * b)`,
  },
};

const initialResult = {
  success: null,
  output: '',
  error: null,
  execution_time_ms: null,
  stage: 'idle',
  statusLabel: 'Ready',
};

function App() {
  const [code, setCode] = useState(defaultCode);
  const [selectedExample, setSelectedExample] = useState('hello');
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [result, setResult] = useState(initialResult);
  const [copied, setCopied] = useState(false);

  const backendLabel = useMemo(() => {
    if (backendStatus === 'connected') return 'Backend: Connected';
    if (backendStatus === 'offline') return 'Backend: Offline';
    return 'Backend: Checking...';
  }, [backendStatus]);

  const backendClass = backendStatus === 'connected' ? 'online' : backendStatus === 'offline' ? 'offline' : 'checking';

  const getStatusLabel = useCallback((stage, success) => {
    if (stage === 'validation') return 'Validation Error';
    if (stage === 'runtime') return 'Runtime Error';
    if (stage === 'timeout') return 'Timeout';
    if (stage === 'backend') return 'Backend Error';
    if (stage === 'completed' || success === true) return 'Success';
    if (stage === 'running') return 'Running';
    return 'Ready';
  }, []);

  const executeCode = useCallback(async () => {
    if (isLoading || !code.trim()) return;

    setIsLoading(true);
    setCopied(false);
    setResult({
      success: null,
      output: '',
      error: null,
      execution_time_ms: null,
      stage: 'running',
      statusLabel: 'Running',
    });

    try {
      const response = await fetch('http://127.0.0.1:8000/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error('Unable to connect to the WASMBOX backend. Make sure the FastAPI server is running.');
      }

      const data = await response.json();

      if (!data || typeof data !== 'object') {
        throw new Error('Malformed response from the WASMBOX backend.');
      }

      const nextStage = data.stage ?? 'completed';
      const nextStatus = getStatusLabel(nextStage, Boolean(data.success));
      setResult({
        success: Boolean(data.success),
        output: data.output ?? '',
        error: data.error ?? null,
        execution_time_ms: data.execution_time_ms ?? null,
        stage: nextStage,
        statusLabel: nextStatus,
      });
    } catch (error) {
      setResult({
        success: false,
        output: '',
        error: error instanceof Error ? error.message : 'Unknown backend error.',
        execution_time_ms: null,
        stage: 'backend',
        statusLabel: 'Backend Error',
      });
    } finally {
      setIsLoading(false);
    }
  }, [code, getStatusLabel, isLoading]);

  useEffect(() => {
    async function checkBackend() {
      setBackendStatus('checking');
      try {
        const response = await fetch('http://127.0.0.1:8000/health');
        setBackendStatus(response.ok ? 'connected' : 'offline');
      } catch (error) {
        setBackendStatus('offline');
      }
    }

    checkBackend();
  }, []);

  useEffect(() => {
    const handleKeyboard = (event) => {
      const isModifier = event.ctrlKey || event.metaKey;
      if (isModifier && event.key === 'Enter') {
        event.preventDefault();
        executeCode();
      }
    };

    window.addEventListener('keydown', handleKeyboard);
    return () => window.removeEventListener('keydown', handleKeyboard);
  }, [executeCode]);

  function clearCode() {
    setCode('');
    setSelectedExample('');
    setResult({
      ...initialResult,
      statusLabel: 'Ready',
    });
    setCopied(false);
  }

  function resetExample() {
    setSelectedExample('hello');
    setCode(examples.hello.code);
    setResult({ ...initialResult, statusLabel: 'Ready' });
    setCopied(false);
  }

  function clearResult() {
    setResult({ ...initialResult, statusLabel: 'Ready' });
    setCopied(false);
  }

  async function copyOutput() {
    const output = result.output || result.error || '';
    if (!output) return;

    try {
      await navigator.clipboard.writeText(output);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (error) {
      setCopied(false);
    }
  }

  function formatExecutionTime(milliseconds) {
    if (milliseconds === null || milliseconds === undefined) return 'n/a';
    if (milliseconds < 1000) return `${Math.round(milliseconds)} ms`;
    return `${(milliseconds / 1000).toFixed(2)} s`;
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-block">
          <div className="brand-row">
            <div className="brand-mark">W</div>
            <div>
              <div className="brand">WASMBOX</div>
              <div className="subtitle">Python execution powered by Pyodide + WebAssembly</div>
            </div>
          </div>
          <div className="tech-badges" aria-label="Technologies used">
            <span>FastAPI</span>
            <span>Pyodide</span>
            <span>WebAssembly</span>
          </div>
        </div>

        <div className={`status-pill ${backendClass}`}>
          <span className="status-dot" aria-hidden="true" />
          {backendLabel}
        </div>
      </header>

      <main className="workspace">
        <section className="panel editor-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Editor</p>
              <h2>Python Input</h2>
            </div>
            <div className="editor-meta">
              {code.length} chars
            </div>
          </div>

          <div className="editor-shell">
            <textarea
              value={code}
              onChange={(event) => {
                setCode(event.target.value);
                setSelectedExample('');
              }}
              className="code-editor"
              spellCheck={false}
              placeholder="Write Python code here..."
              aria-label="Python editor"
            />
          </div>

          <div className="button-row">
            <button onClick={executeCode} disabled={isLoading || !code.trim()} className="primary-button">
              {isLoading ? 'Executing...' : 'Run Code'}
            </button>
            <button className="secondary" onClick={clearCode} disabled={isLoading}>Clear</button>
            <button className="secondary" onClick={resetExample} disabled={isLoading}>Reset Example</button>
          </div>

          <div className="examples-panel">
            <div className="examples-header">
              <span>Examples</span>
            </div>
            <div className="examples">
              {Object.entries(examples).map(([key, example]) => (
                <button
                  key={key}
                  className={`example-card ${selectedExample === key ? 'selected' : ''}`}
                  onClick={() => {
                    setSelectedExample(key);
                    setCode(example.code);
                    setCopied(false);
                  }}
                  type="button"
                >
                  {example.label}
                </button>
              ))}
            </div>
          </div>
        </section>

        <aside className="panel result-panel">
          <div className="panel-header result-header">
            <div>
              <p className="eyebrow">Output</p>
              <h2>Execution Results</h2>
            </div>
            <div className="result-actions">
              <button className="secondary small" onClick={clearResult} type="button">Clear Result</button>
              <button className="secondary small" onClick={copyOutput} type="button" disabled={!result.output && !result.error}>
                {copied ? 'Copied' : 'Copy Output'}
              </button>
            </div>
          </div>

          <div className="result-grid">
            <div className="result-block">
              <span className="label">Status</span>
              <strong className={`status-text ${result.stage === 'validation' ? 'error' : result.stage === 'runtime' ? 'error' : ''}`}>
                {result.statusLabel}
              </strong>
            </div>
            <div className="result-block">
              <span className="label">Stage</span>
              <strong>{result.stage}</strong>
            </div>
            <div className="result-block wide">
              <span className="label">Execution Time</span>
              <strong>{formatExecutionTime(result.execution_time_ms)}</strong>
            </div>
          </div>

          <div className="output-box">
            <div className="panel-label-row">
              <span className="label">Output</span>
            </div>
            <pre className="terminal-output">{result.output || 'No output yet. Run a program to see results here.'}</pre>
          </div>

          {result.error && (
            <div className="error-box">
              <div className="panel-label-row">
                <span className="label">Error</span>
              </div>
              <pre className="terminal-error">{result.error}</pre>
            </div>
          )}

          <div className="info-box">
            <div className="panel-label-row">
              <span className="label">How it works</span>
            </div>
            <ol>
              <li>Write Python code</li>
              <li>Code is validated by FastAPI</li>
              <li>Approved code is sent to the Pyodide worker</li>
              <li>Python executes through WebAssembly</li>
              <li>Output or errors return to the browser</li>
            </ol>
            <p className="prototype-note">
              WASMBOX is a prototype WebAssembly execution environment and is not intended to be a production security sandbox.
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
}

export default App;
