import { useMemo } from "react";

export default function FinancialHealthSummary({ financialHealth, insight }) {
  const { score = 0, riskBand, confidence } = financialHealth || {};

  // ---------------- SMART COLOR LOGIC ----------------
  const gaugeColor = useMemo(() => {
    if (score <= 30) return "#ef4444";   // red
    if (score <= 60) return "#f59e0b";   // orange
    return "#10b981";                    // green
  }, [score]);

  const glowColor = useMemo(() => {
    if (score <= 30) return "shadow-[0_0_35px_rgba(239,68,68,0.6)]";
    if (score <= 60) return "shadow-[0_0_35px_rgba(245,158,11,0.6)]";
    return "shadow-[0_0_35px_rgba(16,185,129,0.6)]";
  }, [score]);

  const dash = 339.292;
  const progress = dash - (dash * score) / 100;

  return (
    <div
      className="
        relative
        rounded-3xl
        border border-white/40
        bg-gradient-to-r from-indigo-200/40 via-purple-200/30 to-cyan-200/40
        backdrop-blur-2xl
        shadow-[0_25px_60px_rgba(0,0,0,0.18)]
        px-8 py-6
        overflow-hidden
      "
    >
      {/* AI moving background */}
      <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_30%_20%,white,transparent_60%)] animate-pulse" />

      <div className="relative flex items-center justify-between">
        {/* LEFT SIDE */}
        <div className="flex items-center gap-6">

          {/* GAUGE */}
          <div className={`relative ${glowColor}`}>
            <svg width="120" height="120">
              <circle
                cx="60"
                cy="60"
                r="54"
                stroke="#e5e7eb"
                strokeWidth="10"
                fill="none"
              />

              <circle
                cx="60"
                cy="60"
                r="54"
                stroke={gaugeColor}
                strokeWidth="10"
                fill="none"
                strokeDasharray={dash}
                strokeDashoffset={progress}
                strokeLinecap="round"
                transform="rotate(-90 60 60)"
                style={{
                  transition: "stroke-dashoffset 1s ease",
                }}
              />
            </svg>

            {/* SCORE */}
            <div className="absolute inset-0 flex items-center justify-center text-3xl font-bold text-gray-900">
              {score}
            </div>
          </div>

          {/* TEXT */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Financial Health
            </h2>

            <p className="text-sm text-gray-700 mt-1">
              Model confidence: {confidence}% — consolidated score
            </p>

            {/* AI INSIGHT */}
            <div className="
              mt-4
              px-4 py-2
              rounded-xl
              bg-white/60
              border border-white/70
              backdrop-blur-md
              text-sm
              font-medium
              text-gray-900
              shadow-sm
            ">
              🤖 {insight}
            </div>
          </div>
        </div>

        {/* RISK BADGE */}
        <div className="
          px-5 py-2
          rounded-full
          text-sm
          font-semibold
          bg-white/50
          border border-white/60
          backdrop-blur-md
          text-gray-900
        ">
          {riskBand}
        </div>
      </div>
    </div>
  );
}
