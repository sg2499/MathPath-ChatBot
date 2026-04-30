import { useMemo, useState } from "react";
import { apiGet, downloadBlob, normalizeBackendUrl } from "./utils/api";
import LoginPanel from "./components/LoginPanel.jsx";
import MetricCard from "./components/MetricCard.jsx";
import LeadTable from "./components/LeadTable.jsx";
import LeadDetailsModal from "./components/LeadDetailsModal.jsx";
import { Activity, Download, Flame, RefreshCw, Search, ShieldCheck, UserCheck, Users } from "lucide-react";

const DEFAULT_BACKEND = import.meta.env.VITE_DEFAULT_BACKEND_URL || "http://localhost:8000";

function calculateMetrics(leads) {
  const total = leads.length;
  const hot = leads.filter((l) => String(l.lead_priority || "").toLowerCase().includes("hot")).length;
  const warm = leads.filter((l) => String(l.lead_priority || "").toLowerCase().includes("warm")).length;
  const consented = leads.filter((l) => l.consent_to_contact === true || String(l.consent_to_contact).toLowerCase() === "true").length;
  return { total, hot, warm, consented };
}

export default function App() {
  const [backendUrl, setBackendUrl] = useState(sessionStorage.getItem("mathpath_admin_backend") || DEFAULT_BACKEND);
  const [adminKey, setAdminKey] = useState(sessionStorage.getItem("mathpath_admin_key") || "");
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [health, setHealth] = useState(null);
  const [leads, setLeads] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);

  const [search, setSearch] = useState("");
  const [priority, setPriority] = useState("all");
  const [mode, setMode] = useState("all");
  const [status, setStatus] = useState("all");

  async function connect() {
    setLoading(true);
    setError("");
    try {
      const normalized = normalizeBackendUrl(backendUrl);
      const healthData = await apiGet("/health", { backendUrl: normalized });
      const leadData = await apiGet("/admin/leads?limit=500", { backendUrl: normalized, adminKey });
      setHealth(healthData);
      setLeads(leadData.leads || []);
      setConnected(true);
      sessionStorage.setItem("mathpath_admin_backend", normalized);
      sessionStorage.setItem("mathpath_admin_key", adminKey);
    } catch (err) {
      setError(err.message || "Unable to connect.");
    } finally {
      setLoading(false);
    }
  }

  async function refreshLeads() {
    setLoading(true);
    setError("");
    try {
      const leadData = await apiGet("/admin/leads?limit=500", { backendUrl, adminKey });
      setLeads(leadData.leads || []);
    } catch (err) {
      setError(err.message || "Unable to refresh leads.");
    } finally {
      setLoading(false);
    }
  }

  async function exportLeads() {
    try {
      const blob = await apiGet("/admin/leads/export", { backendUrl, adminKey, isCsv: true });
      downloadBlob(blob, "mathpath_leads.csv");
    } catch (err) {
      setError(err.message || "Could not export leads.");
    }
  }

  async function exportChats() {
    try {
      const blob = await apiGet("/admin/chat-logs/export", { backendUrl, adminKey, isCsv: true });
      downloadBlob(blob, "mathpath_chat_logs.csv");
    } catch (err) {
      setError(err.message || "Could not export chat logs.");
    }
  }

  const filteredLeads = useMemo(() => {
    const q = search.trim().toLowerCase();
    return leads.filter((lead) => {
      const haystack = [
        lead.parent_name,
        lead.child_name,
        lead.phone,
        lead.email,
        lead.child_class,
        lead.child_age,
        lead.main_concern,
        lead.message,
        lead.recommended_program,
      ].filter(Boolean).join(" ").toLowerCase();
      const matchesSearch = !q || haystack.includes(q);
      const matchesPriority = priority === "all" || String(lead.lead_priority || "new").toLowerCase() === priority;
      const matchesMode = mode === "all" || String(lead.preferred_mode || "not_sure").toLowerCase() === mode;
      const matchesStatus = status === "all" || String(lead.status || "new").toLowerCase() === status;
      return matchesSearch && matchesPriority && matchesMode && matchesStatus;
    });
  }, [leads, search, priority, mode, status]);

  const metrics = calculateMetrics(leads);

  if (!connected) {
    return (
      <LoginPanel
        backendUrl={backendUrl}
        setBackendUrl={setBackendUrl}
        adminKey={adminKey}
        setAdminKey={setAdminKey}
        onConnect={connect}
        loading={loading}
        error={error}
      />
    );
  }

  return (
    <div className="dashboard">
      <header className="topbar">
        <div className="brand-row compact">
          <img src="/MathPath-Logo.png" alt="MathPath" className="brand-logo small" />
          <div>
            <h1>MathPath Chatbot Admin</h1>
            <p>{backendUrl} · {health?.status || "connected"}</p>
          </div>
        </div>
        <div className="header-actions">
          <button onClick={refreshLeads} className="secondary-button" disabled={loading}><RefreshCw size={16} /> Refresh</button>
          <button onClick={exportLeads} className="secondary-button"><Download size={16} /> Leads CSV</button>
          <button onClick={exportChats} className="secondary-button"><Download size={16} /> Chat Logs</button>
        </div>
      </header>

      {error && <div className="error-box dashboard-error">{error}</div>}

      <section className="metrics-grid">
        <MetricCard label="Total Leads" value={metrics.total} hint="All captured enquiries" icon={Users} />
        <MetricCard label="Hot Leads" value={metrics.hot} hint="High-intent parents" icon={Flame} />
        <MetricCard label="Warm Leads" value={metrics.warm} hint="Likely follow-up needed" icon={Activity} />
        <MetricCard label="Consented" value={metrics.consented} hint="Can be contacted" icon={ShieldCheck} />
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Lead Inbox</h2>
            <p>{filteredLeads.length} of {leads.length} leads shown</p>
          </div>
          <div className="filter-row">
            <div className="search-box"><Search size={16} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search parent, phone, concern..." /></div>
            <select value={priority} onChange={(e) => setPriority(e.target.value)}>
              <option value="all">All priorities</option>
              <option value="hot">Hot</option>
              <option value="warm">Warm</option>
              <option value="new">New</option>
            </select>
            <select value={mode} onChange={(e) => setMode(e.target.value)}>
              <option value="all">All modes</option>
              <option value="offline">Offline</option>
              <option value="online">Online</option>
              <option value="hybrid">Hybrid</option>
              <option value="not_sure">Not sure</option>
            </select>
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="all">All statuses</option>
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="demo_booked">Demo booked</option>
              <option value="converted">Converted</option>
              <option value="not_interested">Not interested</option>
            </select>
          </div>
        </div>
        <LeadTable leads={filteredLeads} onOpenLead={setSelectedLead} />
      </section>

      <section className="panel tips-panel">
        <h2><UserCheck size={18} /> Follow-up Priority Guide</h2>
        <p><strong>Hot:</strong> Contact as early as possible. These parents typically asked for admission, demo, fees, callback, or shared strong concern.</p>
        <p><strong>Warm:</strong> Follow up within the same day. These users showed interest in a program, age suitability, bridge course, or practice model.</p>
        <p><strong>New:</strong> General enquiry. Use a soft counselling message and invite them for a demo class.</p>
      </section>

      <LeadDetailsModal lead={selectedLead} onClose={() => setSelectedLead(null)} />
    </div>
  );
}
