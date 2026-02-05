import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

export default function HealthBreakdownCard({ healthBreakdown = [] }) {
  if (!Array.isArray(healthBreakdown) || healthBreakdown.length === 0) {
    return (
      <div className="rounded-xl border p-6 bg-white/10">
        <h3 className="text-sm font-semibold mb-2">Health Breakdown</h3>
        <p className="text-sm opacity-60">No breakdown data available.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-6 bg-white/10">
      <h3 className="text-sm font-semibold mb-4">Health Breakdown</h3>

      <div className="h-[240px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={healthBreakdown}>
            <XAxis dataKey="label" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Bar dataKey="score" fill="#6366f1" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
