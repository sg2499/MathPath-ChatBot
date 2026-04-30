import { useState } from "react";
import { submitLead } from "./api.js";

const initialLead = {
  parent_name: "",
  child_name: "",
  child_age: "",
  child_class: "",
  phone: "",
  email: "",
  preferred_mode: "not_sure",
  main_concern: "",
  preferred_callback_time: "",
  consent_to_contact: true
};

export default function LeadForm({ sessionId, onSubmitted }) {
  const [lead, setLead] = useState(initialLead);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [leadId, setLeadId] = useState("");

  function updateField(event) {
    const { name, value, type, checked } = event.target;
    setLead((current) => ({ ...current, [name]: type === "checkbox" ? checked : value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("submitting");
    setError("");

    try {
      const result = await submitLead({
        ...lead,
        session_id: sessionId,
        source: "mathpath_chatbot_widget"
      });
      setLeadId(result.lead_id || "");
      setStatus("submitted");
      onSubmitted?.(lead);
      setLead(initialLead);
    } catch (err) {
      setError("Unable to submit right now. Please call MathPath at 7980918759 / 9831684229.");
      setStatus("idle");
    }
  }

  if (status === "submitted") {
    return (
      <div className="mp-lead-success">
        <strong>Thank you!</strong> The MathPath team will contact you shortly for demo class and level guidance.
        {leadId && <span className="mp-lead-id">Reference: {leadId}</span>}
      </div>
    );
  }

  return (
    <form className="mp-lead-form" onSubmit={handleSubmit}>
      <h4>Book a Free Demo / Callback</h4>
      <input name="parent_name" value={lead.parent_name} onChange={updateField} placeholder="Parent name" required />
      <input name="child_name" value={lead.child_name} onChange={updateField} placeholder="Child name" />
      <div className="mp-form-grid">
        <input name="child_age" value={lead.child_age} onChange={updateField} placeholder="Age" />
        <input name="child_class" value={lead.child_class} onChange={updateField} placeholder="Class" />
      </div>
      <input name="phone" value={lead.phone} onChange={updateField} placeholder="Phone number" required />
      <input name="email" value={lead.email} onChange={updateField} placeholder="Email" type="email" />
      <select name="preferred_mode" value={lead.preferred_mode} onChange={updateField}>
        <option value="not_sure">Preferred mode: Not sure</option>
        <option value="offline">Offline</option>
        <option value="online">Online</option>
        <option value="hybrid">Hybrid</option>
      </select>
      <input name="main_concern" value={lead.main_concern} onChange={updateField} placeholder="Main concern: speed, basics, school maths..." />
      <input name="preferred_callback_time" value={lead.preferred_callback_time} onChange={updateField} placeholder="Preferred callback time" />
      <label className="mp-consent-row">
        <input
          name="consent_to_contact"
          type="checkbox"
          checked={lead.consent_to_contact}
          onChange={updateField}
          required
        />
        <span>I agree to be contacted by MathPath for demo class and admission guidance.</span>
      </label>
      {error && <p className="mp-form-error">{error}</p>}
      <button type="submit" disabled={status === "submitting"}>
        {status === "submitting" ? "Submitting..." : "Submit Details"}
      </button>
    </form>
  );
}
