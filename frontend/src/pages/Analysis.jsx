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
  const [error, setError] = useState("");

  useEffect(() => {
    getAnalysisData()
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error(err);
        setError("Unable to load analysis data.");
      });
  }, []);

  if (error) {
    return <p className="text-rose-600">{error}</p>;
  }

  if (!data) {
    return <p className="text-slate-700">Loading analysis...</p>;
  }

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-slate-900">
          Financial Analytics
        </h2>
        <p className="text-sm text-slate-600">
          Visual analysis of cash flow, risk, and performance
        </p>
      </div>

      {/* Score Band */}
      <div className="glass-card p-6 mb-8 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">Health Score</p>
          <p className="text-4xl font-bold text-indigo-600">
            {data.health_score ?? "--"}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">Risk Level</p>
          <p
            className={`text-2xl font-semibold ${
              data.risk_level === "High"
                ? "text-rose-600"
                : data.risk_level === "Medium"
                ? "text-amber-600"
                : "text-emerald-600"
            }`}
          >
            {data.risk_level ?? "—"}
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {[
          { label: "Total Revenue", value: data.kpis?.total_revenue },
          { label: "Total Expenses", value: data.kpis?.total_expenses },
          { label: "Net Cash Flow", value: data.kpis?.net_cash_flow },
          { label: "Avg Monthly Cash", value: data.kpis?.avg_monthly_cash },
        ].map((item, i) => (
          <div key={i} className="glass-card p-4">
            <p className="text-xs text-slate-500">{item.label}</p>
            <p className="text-xl font-bold text-slate-900">
              ₹{item.value?.toLocaleString() ?? "—"}
            </p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
        {/* Cash Flow Trend */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-4">
            Cash Flow Trend
          </h3>

          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={data.cash_flow_trend ?? []}>
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

        {/* Inflow vs Outflow */}
        <div className="glass-card p-6">
          <h3 className="font-semibold text-slate-900 mb-4">
            Cash In vs Cash Out
          </h3>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={data.cash_flow_trend ?? []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="inflow" fill="#22c55e" radius={[6, 6, 0, 0]} />
              <Bar dataKey="outflow" fill="#ef4444" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Insights */}
      <div className="glass-card p-6">
        <h3 className="font-semibold text-slate-900 mb-4">
          AI Insights & Recommendations
        </h3>

        <ul className="space-y-3 text-sm">
          {(data.insights ?? []).map((item, i) => {
            const color =
              item.severity === "critical"
                ? "bg-rose-100 text-rose-700"
                : item.severity === "warning"
                ? "bg-amber-100 text-amber-700"
                : "bg-emerald-100 text-emerald-700";

            return (
              <li
                key={i}
                className={`p-3 rounded-xl flex items-start gap-3 ${color}`}
              >
                <span className="mt-1 w-2 h-2 rounded-full bg-current" />
                {item.text}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
