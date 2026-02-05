import { memo } from "react";
import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";

function TrendSignalsCard({ trends }) {
  if (!trends?.length) return null;

  const icons = {
    up: <ArrowUpRight size={16} className="text-emerald-400" />,
    down: <ArrowDownRight size={16} className="text-red-400" />,
    flat: <Minus size={16} className="text-gray-400" />,
  };

  return (
    <div className="rounded-xl border border-white/10 p-5">
      <h3 className="text-sm font-semibold mb-4">Trend Signals</h3>

      <ul className="space-y-3">
        {trends.map((t) => (
          <li key={t.metric} className="flex justify-between items-center">
            <span className="text-sm">{t.metric}</span>
            <div className="flex items-center gap-2">
              {icons[t.direction]}
              <span className="text-xs opacity-60">{t.period}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default memo(TrendSignalsCard);
