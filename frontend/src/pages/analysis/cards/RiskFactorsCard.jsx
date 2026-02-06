import { useEffect, useState } from "react";

export default function RiskFactorsCard({ riskFactors = [] }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 250);
  }, []);

  if (!riskFactors.length) return null;

  const hasHigh = riskFactors.some(r => r.severity === "HIGH");

  const getStyle = (severity) => {
    if (severity === "HIGH")
      return {
        bg: "bg-red-300/25",
        border: "border-red-400/50",
        glow: "0 0 20px rgba(239,68,68,0.45)",
        bar: "from-red-500 to-red-300",
        text: "text-red-900",
      };

    if (severity === "MODERATE")
      return {
        bg: "bg-yellow-300/25",
        border: "border-yellow-400/50",
        glow: "0 0 15px rgba(245,158,11,0.35)",
        bar: "from-yellow-500 to-yellow-300",
        text: "text-yellow-900",
      };

    return {
      bg: "bg-blue-300/20",
      border: "border-blue-400/40",
      glow: "0 0 10px rgba(59,130,246,0.25)",
      bar: "from-blue-500 to-blue-300",
      text: "text-blue-900",
    };
  };

  return (
    <div
      className={`
        relative
        w-full
        rounded-3xl
        border border-white/40
        bg-gradient-to-br from-white/30 to-white/10
        backdrop-blur-2xl
        shadow-[0_25px_60px_rgba(0,0,0,0.18)]
        px-8 py-6
        overflow-hidden
        transition-all duration-700
        ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}
      `}
    >
      {/* GLOBAL DANGER AMBIENT GLOW */}
      {hasHigh && (
        <div
          className="absolute inset-0 pointer-events-none opacity-30"
          style={{
            background:
              "radial-gradient(circle at 15% 20%, rgba(239,68,68,0.35), transparent 60%)",
            animation: "dangerPulse 2.8s ease-in-out infinite",
          }}
        />
      )}

      <h3 className="text-lg font-semibold mb-6 text-gray-900 relative z-10">
        Risk Factors
      </h3>

      <div className="space-y-4 relative z-10">
        {riskFactors.map((r, i) => {
          const style = getStyle(r.severity);

          return (
            <div
              key={i}
              style={{
                transitionDelay: `${i * 120}ms`,
                boxShadow: style.glow,
              }}
              className={`
                group
                rounded-2xl
                border
                ${style.border}
                ${style.bg}
                backdrop-blur-xl
                px-5 py-4
                transition-all duration-500
                hover:scale-[1.02]
                ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
              `}
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className={`text-xs font-semibold ${style.text}`}>
                    {r.severity}
                  </div>

                  <div className="text-sm font-medium text-gray-900">
                    {r.type}
                  </div>
                </div>

                <div className="text-lg font-bold text-gray-900">
                  {r.confidence}%
                </div>
              </div>

              {/* HEAT BAR */}
              <div className="mt-3 h-1.5 w-full rounded-full bg-white/40 overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r ${style.bar}`}
                  style={{
                    width: `${r.confidence}%`,
                    boxShadow: style.glow,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* KEYFRAMES */}
      <style>
        {`
          @keyframes dangerPulse {
            0%,100% { opacity: 0.25; transform: scale(1); }
            50% { opacity: 0.45; transform: scale(1.06); }
          }
        `}
      </style>
    </div>
  );
}
