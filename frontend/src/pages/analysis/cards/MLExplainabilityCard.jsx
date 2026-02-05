export default function MLExplainabilityCard({ ml }) {
  if (!ml) return null;

  return (
    <div className="rounded-xl border p-6 bg-white/10">
      <h3 className="text-sm font-semibold mb-3">AI Explainability</h3>

      <div className="text-sm space-y-2">
        <div>
          Model confidence: <strong>{ml.confidence}%</strong>
        </div>
        <div className="opacity-70">
          Low confidence indicates limited historical data.
        </div>
        <div className="text-xs opacity-60">
          Model version: {ml.model_version}
        </div>
      </div>
    </div>
  );
}
