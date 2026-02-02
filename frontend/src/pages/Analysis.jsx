import { useEffect, useState } from "react";
import { getAnalysisData } from "../api/analysisApi";

export default function Analysis() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalysisData()
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load analysis data.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-slate-600">
        Loading financial analysis…
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-rose-600 font-medium">
        {error}
      </div>
    );
  }

  const bank = data.bank_analysis;
  const gst = data.gst_analysis;
  const risk = data.risk_analysis;

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      {/* ================= HEADER ================= */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Financial Analytics
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Raw financial analysis generated from your uploaded documents
        </p>
      </div>

      {/* ================= SCORE ================= */}
      <div className="glass-card p-6 mb-8 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">Financial Health Score</p>
          <p className="text-4xl font-bold text-indigo-600">
            {data.financial_health_score}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">Risk Level</p>
          <p
            className={`text-2xl font-semibold ${
              data.financial_health_score >= 75
                ? "text-emerald-600"
                : data.financial_health_score >= 50
                ? "text-amber-600"
                : "text-rose-600"
            }`}
          >
            {data.financial_health_score >= 75
              ? "LOW"
              : data.financial_health_score >= 50
              ? "MODERATE"
              : "HIGH"}
          </p>
        </div>
      </div>

      {/* ================= BANK ANALYSIS ================= */}
      <div className="glass-card p-6 mb-8">
        <h3 className="font-semibold text-slate-900 mb-4">
          Bank Analysis
        </h3>

        {bank ? (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
            <Stat label="Total Credits" value={bank.total_credits} />
            <Stat label="Total Debits" value={bank.total_debits} />
            <Stat label="Net Cash Flow" value={bank.net_cash_flow} />
            <Stat label="Closing Balance" value={bank.closing_balance} />
            <Stat
              label="Expense Ratio"
              value={(bank.expense_ratio * 100).toFixed(1) + "%"}
            />
            <Stat
              label="Savings Ratio"
              value={(bank.savings_ratio * 100).toFixed(1) + "%"}
            />
            <Stat
              label="Cashflow Volatile"
              value={bank.cashflow_volatile ? "Yes" : "No"}
            />
          </div>
        ) : (
          <p className="text-slate-500 text-sm">
            No structured bank data found.
          </p>
        )}
      </div>

      {/* ================= GST ANALYSIS ================= */}
      <div className="glass-card p-6 mb-8">
        <h3 className="font-semibold text-slate-900 mb-4">
          GST Analysis
        </h3>

        {gst ? (
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
            <Stat label="Total Taxable Value" value={gst.total_taxable_value} />
            <Stat label="Total GST Paid" value={gst.total_gst} />
            <Stat
              label="Compliance Status"
              value={gst.is_compliant ? "Compliant" : "Not Compliant"}
            />
            <Stat
              label="Payment Ratio"
              value={(gst.payment_ratio * 100).toFixed(1) + "%"}
            />
          </div>
        ) : (
          <p className="text-slate-500 text-sm">
            No GST data available.
          </p>
        )}
      </div>

      {/* ================= RISK ANALYSIS ================= */}
      <div className="glass-card p-6">
        <h3 className="font-semibold text-slate-900 mb-4">
          Risk Analysis
        </h3>

        {risk.priority_issues.length === 0 &&
        risk.warnings.length === 0 ? (
          <p className="text-sm text-emerald-600">
            No major financial risks detected.
          </p>
        ) : (
          <ul className="space-y-3 text-sm">
            {risk.priority_issues.map((item, i) => (
              <li
                key={`p-${i}`}
                className="p-3 rounded-xl bg-rose-100 text-rose-700"
              >
                {item}
              </li>
            ))}
            {risk.warnings.map((item, i) => (
              <li
                key={`w-${i}`}
                className="p-3 rounded-xl bg-amber-100 text-amber-700"
              >
                {item}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

/* ================= SMALL STAT COMPONENT ================= */
function Stat({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="text-lg font-semibold text-slate-900">
        {typeof value === "number" ? `₹${value.toLocaleString()}` : value}
      </p>
    </div>
  );
}
