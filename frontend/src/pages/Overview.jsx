import { useEffect, useState } from "react";
import { getOverviewData } from "../api/overviewApi";

export default function Overview() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getOverviewData().then((res) => setData(res.data));
  }, []);

  if (!data) {
    return <p className="text-slate-700">Loading overview...</p>;
  }

  return (
    <div
      className="min-h-full p-8 rounded-3xl
      bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100"
    >
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Business Overview
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Financial health & performance snapshot
        </p>
      </div>

      {/* Health Score */}
      <div
        className="mb-10 p-8 rounded-3xl
        bg-gradient-to-r from-rose-500 to-pink-500
        text-white shadow-xl"
      >
        <p className="text-sm opacity-90">
          Financial Health Score
        </p>
        <p className="mt-3 text-5xl font-bold">
          {data.health_score ?? "N/A"}
        </p>
        <p className="mt-2 text-sm opacity-90">
          Creditworthiness & stability indicator
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <GlassKpi
          title="Cash Flow"
          value={data.cash_flow_status}
          color="text-emerald-600"
        />

        <GlassKpi
          title="Risk Level"
          value={data.risk_level}
          color="text-amber-600"
        />

        <GlassKpi
          title="Compliance"
          value={data.compliance_status}
          color="text-rose-600"
        />

        <GlassKpi
          title="Credit Exposure"
          value={`₹${(data.credit_exposure / 100000).toFixed(1)} L`}
          color="text-indigo-600"
        />
      </div>

      {/* Bottom Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Coverage */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-1">
            Data Coverage
          </h3>
          <p className="text-sm text-slate-600">
            {data.data_coverage} financial documents processed.
          </p>
        </div>

        {/* Recommendations */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-2">
            Recommended Actions
          </h3>
          <ul className="space-y-2 text-sm text-slate-700">
            {data.recommendations.map((item, i) => (
              <li key={i} className="flex gap-2">
                <span className="mt-1 w-2 h-2 rounded-full bg-rose-500" />
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

/* KPI Card */
function GlassKpi({ title, value, color }) {
  return (
    <div className="glass-card p-5">
      <p className="text-sm text-slate-500">{title}</p>
      <p className={`mt-3 text-2xl font-semibold ${color}`}>
        {value}
      </p>
    </div>
  );
}
