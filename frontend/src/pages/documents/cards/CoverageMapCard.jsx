export default function CoverageMapCard({ coverage }) {
  if (!coverage) return null;

  const Bar = ({ label, value, gradient }) => {
    const safeValue = Math.min(Math.max(Number(value) || 0, 0), 100);

    return (
      <div className="space-y-2">
        <div className="flex justify-between items-center text-sm">
          <span className="font-medium text-gray-800">{label}</span>
          <span className="font-semibold text-gray-900">{safeValue}%</span>
        </div>

        <div className="relative w-full h-3 bg-white/40 backdrop-blur-sm rounded-full overflow-hidden">
          <div
            className={`h-3 rounded-full transition-all duration-700 ease-out ${gradient}`}
            style={{ width: `${safeValue}%` }}
          />

          {/* glow layer */}
          <div
            className={`absolute top-0 left-0 h-3 blur-md opacity-40 ${gradient}`}
            style={{ width: `${safeValue}%` }}
          />
        </div>
      </div>
    );
  };

  return (
    <div
      className="
        relative
        p-7
        rounded-3xl
        shadow-xl
        border border-white/30
        bg-white/30
        backdrop-blur-xl
        transition-all duration-300
        hover:shadow-2xl
        hover:-translate-y-1
      "
    >
      {/* background glow */}
      <div className="absolute -top-10 -right-10 w-40 h-40 bg-purple-400/30 blur-3xl rounded-full"></div>
      <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-blue-400/30 blur-3xl rounded-full"></div>

      <div className="relative">
        <h3 className="text-lg font-semibold mb-6 text-gray-900">
          Coverage Map
        </h3>

        <div className="space-y-6">
          <Bar
            label="Bank"
            value={coverage && coverage.BANK}
            gradient="bg-gradient-to-r from-blue-500 to-indigo-500"
          />

          <Bar
            label="GST"
            value={coverage && coverage.GST}
            gradient="bg-gradient-to-r from-emerald-500 to-green-500"
          />

          <Bar
            label="Financials"
            value={coverage && coverage.FINANCIALS}
            gradient="bg-gradient-to-r from-purple-500 to-fuchsia-500"
          />
        </div>
      </div>
    </div>
  );
}
