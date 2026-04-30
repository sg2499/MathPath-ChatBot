import { X, Phone, Mail, UserRound, MessageCircle } from "lucide-react";

function Row({ label, value }) {
  return (
    <div className="detail-row">
      <span>{label}</span>
      <strong>{value || "—"}</strong>
    </div>
  );
}

export default function LeadDetailsModal({ lead, onClose }) {
  if (!lead) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><X size={18} /></button>
        <div className="modal-header">
          <img src="/MathPath-Logo.png" alt="MathPath" />
          <div>
            <h2>{lead.parent_name || "Lead Details"}</h2>
            <p>{lead.lead_id}</p>
          </div>
        </div>

        <div className="detail-grid">
          <Row label="Created" value={lead.created_at ? new Date(lead.created_at).toLocaleString() : "—"} />
          <Row label="Priority" value={`${lead.lead_priority || "new"} (${lead.lead_score ?? "—"})`} />
          <Row label="Status" value={lead.status || "new"} />
          <Row label="Recommended Program" value={lead.recommended_program} />
          <Row label="Preferred Mode" value={lead.preferred_mode} />
          <Row label="Callback Time" value={lead.preferred_callback_time} />
        </div>

        <div className="contact-actions">
          {lead.phone && <a href={`tel:${lead.phone}`}><Phone size={16} /> Call</a>}
          {lead.email && <a href={`mailto:${lead.email}`}><Mail size={16} /> Email</a>}
        </div>

        <div className="section-title"><UserRound size={16} /> Child Information</div>
        <div className="detail-grid">
          <Row label="Child Name" value={lead.child_name} />
          <Row label="Child Age" value={lead.child_age} />
          <Row label="Child Class" value={lead.child_class} />
          <Row label="Consent" value={lead.consent_to_contact ? "Yes" : "No"} />
        </div>

        <div className="section-title"><MessageCircle size={16} /> Parent Concern / Message</div>
        <div className="message-box">
          <p><strong>Main concern:</strong> {lead.main_concern || "—"}</p>
          <p><strong>Message:</strong> {lead.message || "—"}</p>
          <p><strong>Session:</strong> {lead.session_id || "—"}</p>
          <p><strong>Source:</strong> {lead.source || "—"}</p>
        </div>
      </div>
    </div>
  );
}
