import { memo, useEffect, useState } from "react";
import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";

function TrendSignalsCard({ trends = [] }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 300);
  }, []);

  if (!trends?.length) return null;

  const getStyle = (direction) => {
    if (direction === "up")
      return {
        icon: <ArrowUpRight size={16} />,
        color: "text-emerald-700",
        bg: "bg-emerald-300/25",
        glow: "0 0 12px rgba(16,185,129,0.45)",
      };

    if (direction === "down")
      return {
        icon: <ArrowDownRight size={16} />,
        color: "text-red-700",
        bg: "bg-red-300/25",
        glow: "0 0 12px rgba(239,68,68,0.45)",
      };

    return {
      icon: <Minus size={16} />,
      color: "text-gray-700",
      bg: "bg-gray-300/20",
      glow: "0 0 8px rgba(107,114,128,0.25)",
    };
  };

  return (
    <div
      className={`
        relative
        rounded-3xl
        border border-white/40
        bg-gradient-to-br from-white/30 to-white/10
        backdrop-blur-2xl
        shadow-[0_25px_60px_rgba(0,0,0,0.18)]
        p-7
        overflow-hidden
        transition-all duration-700
        ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}
      `}
    >
      {/* AI ambient layer */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          background:
            "radial-gradient(circle at 25% 30%, rgba(99,102,241,0.35), transparent 60%), radial-gradient(circle at 75% 70%, rgba(16,185,129,0.25), transparent 60%)",
        }}
      />

      <h3 className="text-lg font-semibold mb-5 text-gray-900 relative z-10">
        Trend Signals
      </h3>

      <ul className="space-y-3 relative z-10">
        {trends.map((t, i) => {
          const style = getStyle(t.direction);

          return (
            <li
              key={t.metric}
              style={{
                transitionDelay: `${i * 120}ms`,
                boxShadow: style.glow,
              }}
              className={`
                flex justify-between items-center
                rounded-2xl
                border border-white/40
                ${style.bg}
                backdrop-blur-xl
                px-5 py-4
                transition-all duration-500
                hover:scale-[1.02]
                ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
              `}
            >
              {/* LEFT */}
              <span className="text-sm font-medium text-gray-900">
                {t.metric}
              </span>

              {/* RIGHT */}
              <div className="flex items-center gap-3">
                <div
                  className={`p-2 rounded-lg ${style.color}`}
                  style={{ boxShadow: style.glow }}
                >
                  {style.icon}
                </div>

                <span className="text-xs text-gray-700">
                  {t.period}
                </span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default memo(TrendSignalsCard);
