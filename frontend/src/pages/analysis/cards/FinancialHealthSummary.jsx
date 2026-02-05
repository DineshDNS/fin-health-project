export default function FinancialHealthSummary({ financialHealth }) {
  const { score, riskBand, confidence } = financialHealth || {};

  return (
    <div className="rounded-xl border border-blue-300/60 bg-white/20 p-6">
      <div className="flex justify-between mb-2">
        <h2 className="text-lg font-semibold">Financial Health</h2>
        <span className="text-xs uppercase text-blue-500">
          {riskBand || "INFO"}
        </span>
      </div>

      <div className="text-3xl font-bold mb-1">
        {score ?? "Not Available"}
      </div>

      <p className="text-sm opacity-70">
        Model confidence: {confidence}% — consolidated financial health score.
      </p>
    </div>
  );
}
