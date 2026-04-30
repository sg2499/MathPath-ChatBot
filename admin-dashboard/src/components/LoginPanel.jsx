import { Lock, Server } from "lucide-react";

export default function LoginPanel({ backendUrl, setBackendUrl, adminKey, setAdminKey, onConnect, loading, error }) {
  return (
    <div className="login-page">
      <div className="login-card">
        <div className="brand-row">
          <img src="/MathPath-Logo.png" alt="MathPath" className="brand-logo" />
          <div>
            <h1>MathPath Admin</h1>
            <p>Lead and chatbot monitoring dashboard</p>
          </div>
        </div>

        <label className="field-label">
          <Server size={16} /> Backend URL
        </label>
        <input
          value={backendUrl}
          onChange={(e) => setBackendUrl(e.target.value)}
          placeholder="http://localhost:8000"
          className="input"
        />

        <label className="field-label">
          <Lock size={16} /> Admin API Key
        </label>
        <input
          value={adminKey}
          onChange={(e) => setAdminKey(e.target.value)}
          placeholder="Enter ADMIN_API_KEY from backend .env"
          type="password"
          className="input"
        />

        {error && <div className="error-box">{error}</div>}

        <button className="primary-button" onClick={onConnect} disabled={loading}>
          {loading ? "Connecting..." : "Open Dashboard"}
        </button>

        <p className="small-note">
          The key is stored only in this browser session. For production, keep this dashboard behind a private admin route.
        </p>
      </div>
    </div>
  );
}
