const SEVERITY = {
  DANGER: "border-red-400 bg-red-200/40 text-red-700",
  WARNING: "border-yellow-400 bg-yellow-200/40 text-yellow-700",
  INFO: "border-blue-400 bg-blue-200/40 text-blue-700",
};

export default function RiskFactorsCard({ riskFactors }) {
  if (!riskFactors.length) {
    return (
      <div className="rounded-xl border p-6 bg-white/10">
        <h3 className="text-sm font-semibold mb-2">Risk Factors</h3>
        <p className="text-sm opacity-60">No major risks detected.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-6 bg-white/10">
      <h3 className="text-sm font-semibold mb-4">Risk Factors</h3>

      <div className="space-y-3">
        {riskFactors.map((r, i) => (
          <div
            key={i}
            className={`rounded-lg border p-4 flex justify-between ${
              SEVERITY[r.severity] || SEVERITY.INFO
            }`}
          >
            <div>
              <div className="text-xs font-semibold">{r.severity}</div>
              <div className="text-sm">{r.type}</div>
            </div>
            <div className="font-semibold">{r.confidence}%</div>
          </div>
        ))}
      </div>
    </div>
  );
}
