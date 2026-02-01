export default function RiskAlerts({ riskFlags }) {
  const warnings = riskFlags?.warnings || [];
  const priorityIssues = riskFlags?.priority_issues || [];

  if (warnings.length === 0 && priorityIssues.length === 0) {
    return (
      <div className="glass-card p-6 mb-8">
        <h3 className="font-semibold text-slate-900 mb-1">
          Risk Alerts
        </h3>
        <p className="text-sm text-slate-600">
          No significant risk alerts detected based on available data.
        </p>
      </div>
    );
  }

  return (
    <div className="mb-8">
      <h3 className="font-semibold text-slate-900 mb-4">
        Risk Alerts
      </h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Priority Issues */}
        {priorityIssues.length > 0 && (
          <div className="glass-card p-6 border-l-4 border-rose-500">
            <p className="text-sm font-semibold text-rose-600 mb-2">
              Priority Issues
            </p>
            <ul className="space-y-2 text-sm text-slate-700">
              {priorityIssues.map((item, index) => (
                <li key={index} className="flex gap-2">
                  <span className="mt-1 w-2 h-2 rounded-full bg-rose-500" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Warnings */}
        {warnings.length > 0 && (
          <div className="glass-card p-6 border-l-4 border-amber-400">
            <p className="text-sm font-semibold text-amber-600 mb-2">
              Warnings
            </p>
            <ul className="space-y-2 text-sm text-slate-700">
              {warnings.map((item, index) => (
                <li key={index} className="flex gap-2">
                  <span className="mt-1 w-2 h-2 rounded-full bg-amber-400" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
