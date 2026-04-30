export default function MetricCard({ label, value, hint, icon: Icon }) {
  return (
    <div className="metric-card">
      <div>
        <p className="metric-label">{label}</p>
        <h2>{value}</h2>
        {hint && <p className="metric-hint">{hint}</p>}
      </div>
      {Icon && <Icon className="metric-icon" size={28} />}
    </div>
  );
}
