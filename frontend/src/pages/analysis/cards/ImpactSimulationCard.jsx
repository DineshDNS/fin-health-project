export default function ImpactSimulationCard({ impactSimulation = [] }) {
  if (!impactSimulation.length) {
    return (
      <div className="rounded-xl border p-6 bg-white/10">
        <h3 className="text-sm font-semibold mb-2">Impact Simulation</h3>
        <p className="text-sm opacity-60">No simulations available.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-6 bg-white/10">
      <h3 className="text-sm font-semibold mb-4">Impact Simulation</h3>

      <div className="space-y-3 text-sm">
        {impactSimulation.map((s, i) => (
          <div key={i} className="border rounded-lg p-3 bg-white/20">
            <div className="font-medium">{s.action}</div>
            <div className="opacity-70">
              {s.timeframe} — {s.expected_outcome}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
