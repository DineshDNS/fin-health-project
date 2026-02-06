import { useEffect, useState } from "react";

export default function MLExplainabilityCard({ ml }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 180);
  }, []);

  if (!ml) return null;

  const confidenceColor =
    ml.confidence >= 75
      ? "#10b981"
      : ml.confidence >= 45
      ? "#f59e0b"
      : "#ef4444";

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
      {/* AI AMBIENT BACKGROUND */}
      <div
        className="absolute inset-0 opacity-25 pointer-events-none"
        style={{
          background: `
            radial-gradient(circle at 20% 30%, rgba(99,102,241,0.35), transparent 60%),
            radial-gradient(circle at 80% 70%, rgba(16,185,129,0.25), transparent 60%)
          `,
          animation: "aiPulse 5s ease-in-out infinite",
        }}
      />

      {/* HEADER */}
      <div className="relative z-10 flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          AI Explainability
        </h3>

        <div className="
          text-xs px-3 py-1 rounded-full
          bg-indigo-100 text-indigo-700 font-semibold
        ">
          Model {ml.model_version}
        </div>
      </div>

      {/* CONFIDENCE METER */}
      <div className="relative z-10 mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-700">Model Confidence</span>
          <span
            className="font-semibold"
            style={{ color: confidenceColor }}
          >
            {ml.confidence}%
          </span>
        </div>

        <div className="w-full h-3 rounded-full bg-white/40 overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-1000"
            style={{
              width: `${ml.confidence}%`,
              background: confidenceColor,
              boxShadow: `0 0 10px ${confidenceColor}55`,
            }}
          />
        </div>
      </div>

      {/* AI INTERPRETATION */}
      <div className="relative z-10 text-sm text-gray-800">
        <p className="leading-relaxed">
          This confidence score reflects how strongly the AI model
          trusts the financial patterns detected from uploaded
          documents. Lower confidence may indicate limited historical
          data or incomplete financial coverage.
        </p>
      </div>

      {/* FOOT NOTE */}
      <div className="relative z-10 mt-5 text-xs text-gray-600">
        AI continuously improves accuracy as more data is uploaded.
      </div>

      {/* KEYFRAMES */}
      <style>
        {`
          @keyframes aiPulse {
            0%, 100% { opacity: 0.25; transform: scale(1); }
            50% { opacity: 0.35; transform: scale(1.05); }
          }
        `}
      </style>
    </div>
  );
}
