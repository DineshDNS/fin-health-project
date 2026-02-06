import { useEffect, useState } from "react";

export default function ImpactSimulationCard({ impactSimulation = [] }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 120);
  }, []);

  if (!impactSimulation.length) {
    return (
      <div className="
        rounded-3xl border border-white/40
        bg-white/25 backdrop-blur-2xl
        shadow-xl p-6
      ">
        <h3 className="text-lg font-semibold mb-2 text-gray-900">
          Impact Simulation
        </h3>
        <p className="text-sm text-gray-600">
          No simulations available.
        </p>
      </div>
    );
  }

  return (
    <div
      className={`
        relative rounded-3xl border border-white/40
        bg-gradient-to-br from-white/30 to-white/10
        backdrop-blur-2xl
        shadow-[0_20px_60px_rgba(0,0,0,0.18)]
        p-7
        overflow-hidden
        transition-all duration-700
        ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}
      `}
    >
      {/* Ambient AI background glow */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          background:
            "radial-gradient(circle at 20% 30%, rgba(99,102,241,0.25), transparent 60%), radial-gradient(circle at 80% 70%, rgba(16,185,129,0.25), transparent 60%)",
        }}
      />

      <h3 className="text-lg font-semibold mb-5 text-gray-900 relative z-10">
        Impact Simulation
      </h3>

      <div className="space-y-4 relative z-10">
        {impactSimulation.map((s, i) => (
          <div
            key={i}
            className="
              group
              rounded-2xl
              border border-white/40
              bg-white/40
              backdrop-blur-xl
              p-4
              transition-all duration-300
              hover:scale-[1.015]
              hover:shadow-[0_12px_30px_rgba(0,0,0,0.18)]
            "
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="font-semibold text-gray-900 text-sm">
                  {s.action}
                </div>

                <div className="text-xs text-gray-600 mt-1">
                  {s.timeframe}
                </div>
              </div>

              <div className="
                text-xs font-semibold px-3 py-1 rounded-full
                bg-indigo-100 text-indigo-700
                group-hover:bg-indigo-200
                transition
              ">
                AI Suggestion
              </div>
            </div>

            <div className="text-sm text-gray-700 mt-2">
              {s.expected_outcome}
            </div>

            {/* Progress accent line */}
            <div className="mt-3 h-1 w-full rounded-full bg-gradient-to-r from-indigo-500 to-emerald-400 opacity-60" />
          </div>
        ))}
      </div>
    </div>
  );
}
