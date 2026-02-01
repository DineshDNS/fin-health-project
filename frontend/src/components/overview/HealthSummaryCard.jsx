export default function HealthSummaryCard({ score, riskLevel }) {
  const riskColor =
    riskLevel === "Low"
      ? "text-emerald-600"
      : riskLevel === "Medium"
      ? "text-amber-600"
      : riskLevel === "High"
      ? "text-rose-600"
      : "text-slate-500";

  return (
    <div
      className="mb-10 p-8 rounded-3xl
      bg-white/70 backdrop-blur
      shadow-xl border border-white/40"
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
        {/* Health Score */}
        <div>
          <p className="text-sm text-slate-500">
            Financial Health Score
          </p>
          <p className="mt-2 text-5xl font-bold text-slate-900">
            {score !== null && score !== undefined ? score : "--"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Score range: 0 (poor) → 100 (excellent)
          </p>
        </div>

        {/* Risk Level */}
        <div className="text-right">
          <p className="text-sm text-slate-500">
            Overall Risk Level
          </p>
          <p
            className={`mt-3 text-2xl font-semibold ${riskColor}`}
          >
            {riskLevel ?? "Unknown"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Based on financial stability indicators
          </p>
        </div>
      </div>
    </div>
  );
}
