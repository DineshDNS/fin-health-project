
import { useEffect, useState } from "react";
import { getAnalysisData } from "../api/analysisApi";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
} from "recharts";

export default function Analysis() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAnalysisData().then((res) => setData(res.data));
  }, []);

  if (!data) {
    return <p className="text-slate-700">Loading analysis...</p>;
  }

  return (
    <div
      className="min-h-full p-8 rounded-3xl
      bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100"
    >
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-slate-900">
          Financial Analytics
        </h2>
        <p className="text-sm text-slate-600">
          Visual analysis of cash flow, risk, and performance
        </p>
      </div>

      {/* Score Band (DIFFERENT from Overview) */}
      <div className="glass-card p-6 mb-10 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">Health Score</p>
          <p className="text-4xl font-bold text-indigo-600">
            {data.health_score ?? "--"}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">Risk Level</p>
          <p className="text-2xl font-semibold text-amber-600">
            {data.risk_level}
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">

        {/* Cash Flow Trend */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-4">
            Cash Flow Trend
          </h3>

          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={data.cash_flow_trend}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="net_flow"
                stroke="#6366f1"
                strokeWidth={4}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Net Cash Comparison */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-4">
            Net Cash Comparison
          </h3>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={data.cash_flow_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="net_flow"
                fill="#ec4899"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

      </div>

      {/* AI Insights */}
      <div className="glass-card p-6">
        <h3 className="font-semibold text-slate-900 mb-2">
          AI Insights & Recommendations
        </h3>

        <ul className="space-y-2 text-sm text-slate-700">
          {data.insights.map((item, i) => (
            <li key={i} className="flex gap-2">
              <span className="mt-1 w-2 h-2 rounded-full bg-indigo-500" />
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
