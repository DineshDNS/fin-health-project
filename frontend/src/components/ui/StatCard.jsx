export default function StatCard({ label, value, subtext, badge }) {
  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-black/5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">{label}</p>

        {badge && (
          <span
            className={`px-2 py-0.5 rounded-full text-xs font-medium ${badge.bg} ${badge.color}`}
          >
            {badge.label}
          </span>
        )}
      </div>

      <p className="mt-2 text-2xl font-semibold text-slate-900">
        {value}
      </p>

      {subtext && (
        <p className="mt-1 text-xs text-slate-400">{subtext}</p>
      )}
    </div>
  );
}
