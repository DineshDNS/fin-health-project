import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

export default function HealthBreakdownCard({ healthBreakdown = [] }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setTimeout(() => setShow(true), 150);
  }, []);

  if (!healthBreakdown.length) return null;

  const COLORS = ["#10b981", "#06b6d4", "#6366f1", "#8b5cf6"];

  return (
    <div
      className={`
        w-full rounded-3xl
        bg-white/25 backdrop-blur-2xl border border-white/40 shadow-xl
        px-8 py-6
        transition-all duration-700 ease-out
        ${show ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}
      `}
    >
      <h3 className="text-lg font-semibold mb-4">
        Financial Health Breakdown
      </h3>

      <div className="flex items-center gap-10 h-[240px]">

        {/* BAR CHART */}
        <div className="w-1/2 h-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={healthBreakdown}>
              <XAxis dataKey="label" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar
                dataKey="score"
                radius={[6, 6, 0, 0]}
                fill="#6366f1"
                animationDuration={900}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* DONUT */}
        <div className="w-1/2 h-full flex items-center justify-center">
          <div className="transition-transform duration-700 hover:scale-105">
            <ResponsiveContainer width={240} height={240}>
              <PieChart>
                <Pie
                  data={healthBreakdown}
                  dataKey="score"
                  nameKey="label"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  animationDuration={900}
                >
                  {healthBreakdown.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Legend verticalAlign="bottom" height={30} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
