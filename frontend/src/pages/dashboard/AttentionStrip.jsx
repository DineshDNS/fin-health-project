export default function AttentionStrip({ data }) {
  if (!data) return null;

  // Hide completely for LOW severity
  if (data.severity === "LOW") return null;

  const severityStyles = {
    HIGH: "border-l-red-500 bg-white/40",
    MEDIUM: "border-l-amber-400 bg-white/40",
  };

  return (
    <div
      className={`rounded-xl border border-black/5 border-l-4 p-4
      ${severityStyles[data.severity]}`}
    >
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">
            {data.title}
          </h3>
          <p className="text-xs text-slate-700 mt-1">
            <span className="font-medium">Issue:</span> {data.issue}
          </p>
        </div>

        <div className="text-xs text-slate-600 md:text-right">
          <p>
            <span className="font-medium">Timeframe:</span>{" "}
            {data.timeframe}
          </p>
          <p>
            <span className="font-medium">Impact:</span>{" "}
            {data.impact}
          </p>
        </div>
      </div>
    </div>
  );
}
