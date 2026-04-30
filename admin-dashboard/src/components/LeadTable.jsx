import { Eye } from "lucide-react";

function priorityClass(priority) {
  const normalized = String(priority || "new").toLowerCase();
  if (normalized.includes("hot")) return "pill hot";
  if (normalized.includes("warm")) return "pill warm";
  return "pill new";
}

export default function LeadTable({ leads, onOpenLead }) {
  if (!leads.length) {
    return <div className="empty-state">No leads found for the selected filters.</div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Created</th>
            <th>Parent</th>
            <th>Child</th>
            <th>Class/Age</th>
            <th>Phone</th>
            <th>Mode</th>
            <th>Priority</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.lead_id}>
              <td>{lead.created_at ? new Date(lead.created_at).toLocaleString() : "—"}</td>
              <td>
                <strong>{lead.parent_name || "—"}</strong>
                <span>{lead.email || ""}</span>
              </td>
              <td>{lead.child_name || "—"}</td>
              <td>{[lead.child_class, lead.child_age].filter(Boolean).join(" / ") || "—"}</td>
              <td>{lead.phone || "—"}</td>
              <td>{lead.preferred_mode || "—"}</td>
              <td><span className={priorityClass(lead.lead_priority)}>{lead.lead_priority || "new"}</span></td>
              <td>{lead.status || "new"}</td>
              <td>
                <button className="icon-button" onClick={() => onOpenLead(lead)} title="View details">
                  <Eye size={17} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
