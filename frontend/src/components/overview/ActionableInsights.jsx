export default function ActionableInsights({ insights }) {
  if (!insights || insights.length === 0) {
    return (
      <div className="glass-card p-6">
        <h3 className="font-semibold text-slate-900 mb-2">
          Actionable Insights
        </h3>
        <p className="text-sm text-slate-600">
          Actionable insights will be generated once sufficient financial data is available.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card p-6">
      <h3 className="font-semibold text-slate-900 mb-4">
        Actionable Insights
      </h3>

      <ul className="space-y-3 text-sm text-slate-700">
        {insights.map((item, index) => (
          <li key={index} className="flex gap-3">
            <span className="mt-1 w-2 h-2 rounded-full bg-indigo-500 shrink-0" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
