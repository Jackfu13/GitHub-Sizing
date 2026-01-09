const { useState } = React;

function App() {
  const [repo, setRepo] = useState("");
  const [token, setToken] = useState("");
  const [includeRaw, setIncludeRaw] = useState(false);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [commitCount, setCommitCount] = useState(null);
  const [commitWarning, setCommitWarning] = useState("");

  const isLoading = status === "loading";
  const filtered = data ? data.filtered : null;
  const warnings = data && data.warnings ? data.warnings : [];
  const warningMessages = warnings.map((warning) =>
    `${warning.message} ${warning.details || ""}`.trim()
  );
  if (commitWarning) {
    warningMessages.push(commitWarning);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus("loading");
    setError("");
    setData(null);
    setCommitCount(null);
    setCommitWarning("");

    const payload = {
      repo: repo.trim(),
      include_raw: includeRaw,
    };
    if (token.trim()) {
      payload.token = token.trim();
    }

    try {
      const response = await fetch("/api/github-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      if (!response.ok) {
        const message =
          result.message || result.error || `Request failed with ${response.status}`;
        throw new Error(message);
      }

      setData(result);
      try {
        const commitPayload = { repo: repo.trim() };
        if (token.trim()) {
          commitPayload.token = token.trim();
        }
        const commitResponse = await fetch("/api/commit-count", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(commitPayload),
        });
        const commitResult = await commitResponse.json();
        if (!commitResponse.ok) {
          const message =
            commitResult.message ||
            commitResult.error ||
            `Commit count failed with ${commitResponse.status}`;
          setCommitWarning(message);
        } else {
          setCommitCount(commitResult.commitCount);
        }
      } catch (commitError) {
        setCommitWarning(
          commitError.message || "Commit count request failed."
        );
      }

      setStatus("success");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  };

  return (
    <div className="app">
      <section className="hero">
        <h1>GitHub repo sizing at a glance.</h1>
        <p>
          Drop a repo, optionally add a token for collaborator access, and get a
          clean breakdown plus raw JSON.
        </p>
      </section>

      <section className="panel">
        <header>
          <div>
            <div className="badge">GitHub Inspector</div>
          </div>
          <span className="status">
            {status === "loading" && "Fetching GitHub data..."}
            {status === "success" && "Ready"}
            {status === "error" && "Needs attention"}
          </span>
        </header>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="repo">Repository</label>
            <input
              id="repo"
              type="text"
              placeholder="owner/repo or https://github.com/owner/repo"
              value={repo}
              onChange={(event) => setRepo(event.target.value)}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="token">Personal access token (optional)</label>
            <input
              id="token"
              type="password"
              placeholder="Adds collaborator access for private repos"
              value={token}
              onChange={(event) => setToken(event.target.value)}
            />
          </div>

          <div className="row">
            <label className="toggle">
              <input
                type="checkbox"
                checked={includeRaw}
                onChange={(event) => setIncludeRaw(event.target.checked)}
              />
              Include raw JSON payload
            </label>
            <button type="submit" disabled={isLoading}>
              {isLoading ? "Checking..." : "Get repo data"}
            </button>
          </div>
        </form>

        {error && <div className="error">{error}</div>}

        {warningMessages.length > 0 && (
          <div className="warning">
            {warningMessages.map((message, index) => (
              <div key={`${index}-${message}`}>{message}</div>
            ))}
          </div>
        )}

        {filtered && (
          <div className="results">
            <div className="stats">
              <div className="stat-card">
                <h3>Repo</h3>
                <p>{filtered.repoName}</p>
              </div>
              <div className="stat-card">
                <h3>Owner</h3>
                <p>{filtered.owner}</p>
              </div>
              <div className="stat-card">
                <h3>Size (KB)</h3>
                <p>{filtered.size}</p>
              </div>
              <div className="stat-card">
                <h3>Collaborators</h3>
                <p>{filtered.collaborators.length}</p>
              </div>
              <div className="stat-card">
                <h3>Commits</h3>
                <p>{commitCount === null ? "—" : commitCount}</p>
              </div>
            </div>

            <div className="collab-list">
              {filtered.collaborators.length === 0 && (
                <div className="stat-card">
                  <h3>No collaborators returned</h3>
                  <p>Add a token with repo access to see collaborators.</p>
                </div>
              )}
              {filtered.collaborators.map((collaborator) => (
                <div className="collab-item" key={collaborator.id}>
                  <strong>{collaborator.username}</strong>
                  <span>ID {collaborator.id}</span>
                </div>
              ))}
            </div>

            {includeRaw && data.raw && (
              <pre className="raw-block">
                {JSON.stringify(data.raw, null, 2)}
              </pre>
            )}
          </div>
        )}
      </section>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
