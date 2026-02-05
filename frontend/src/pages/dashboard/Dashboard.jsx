import { useOverview } from "../../hooks/useOverview";
import DashboardSkeleton from "./DashboardSkeleton";
import AttentionStrip from "./AttentionStrip";

/* ===================================================== */
/* DASHBOARD */
/* ===================================================== */

export default function Dashboard() {
  const { data, isLoading, isError } = useOverview();

  if (isLoading) return <DashboardSkeleton />;

  if (isError || !data?.data) {
    return (
      <div className="text-sm text-red-600">
        Failed to load dashboard. Please check API connection.
      </div>
    );
  }

  const {
    business_context,
    health_summary,
    risk_summary,
    key_insights,
    attention_summary,
  } = data.data;

  return (
    <div className="relative min-h-full p-4 dashboard-bg">
      {/* ================= HEADER ================= */}
      <section className="flex items-start justify-between mb-3">
        <div>
          <h1 className="text-lg font-semibold text-slate-900">
            Dashboard
          </h1>
          <p className="text-[11px] text-slate-600">
            Overall financial health snapshot
          </p>
        </div>

        <div className="text-[11px] text-slate-600">
          Last updated: {business_context.last_updated}
        </div>
      </section>

      {/* ================= MAIN CARDS ================= */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MainCard severity={health_summary.ui.severity}>
          <CardLabel>Health Score</CardLabel>
          <CardValue>{health_summary.financial_health_score}</CardValue>
          <CardSubtext>{health_summary.health_label}</CardSubtext>
          <CardMeta>Overall financial health</CardMeta>
        </MainCard>

        <MainCard severity="warning">
          <CardLabel>Credit Readiness</CardLabel>
          <CardValue>{health_summary.credit_readiness}</CardValue>
          <CardMeta>Loan eligibility status</CardMeta>
        </MainCard>

        <MainCard severity={risk_summary.ui.severity}>
          <CardLabel>Overall Risk</CardLabel>
          <CardValue>{risk_summary.overall_risk_level}</CardValue>
          <CardMeta>Financial & ML signals</CardMeta>
        </MainCard>
      </section>

      {/* ================= ATTENTION STRIP ================= */}
      {attention_summary && (
        <div className="mt-5">
          <AttentionStrip data={attention_summary} />
        </div>
      )}

      {/* ================= BUSINESS CONTEXT ================= */}
      <section className="mt-7">
        <h2 className="text-sm font-medium text-slate-900 mb-3">
          Business Context
        </h2>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <ContextCard severity="info">
            <CardLabel>Industry</CardLabel>
            <CardValue>{business_context.industry}</CardValue>
          </ContextCard>

          <ContextCard
            severity={business_context.data_availability.bank ? "success" : "danger"}
          >
            <CardLabel>Bank Data</CardLabel>
            <CardValue>
              {business_context.data_availability.bank ? "Available" : "Missing"}
            </CardValue>
          </ContextCard>

          <ContextCard
            severity={business_context.data_availability.gst ? "success" : "danger"}
          >
            <CardLabel>GST Data</CardLabel>
            <CardValue>
              {business_context.data_availability.gst ? "Available" : "Missing"}
            </CardValue>
          </ContextCard>

          <ContextCard
            severity={business_context.data_availability.financials ? "success" : "danger"}
          >
            <CardLabel>Financial Data</CardLabel>
            <CardValue>
              {business_context.data_availability.financials
                ? "Available"
                : "Missing"}
            </CardValue>
          </ContextCard>
        </div>
      </section>

      {/* ================= KEY INSIGHTS ================= */}
      <section className="mt-7">
        <h2 className="text-sm font-medium text-slate-900 mb-3">
          Key Insights
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {key_insights?.top_risk && (
            <InsightCard
              severity={key_insights.top_risk.ui.severity}
              title={key_insights.top_risk.title}
              badge={key_insights.top_risk.ui.badge}
              text={key_insights.top_risk.summary}
              impact={key_insights.top_risk.why_it_matters}
            />
          )}

          {key_insights?.recommended_action && (
            <InsightCard
              severity={key_insights.recommended_action.ui.severity}
              title={key_insights.recommended_action.title}
              badge={key_insights.recommended_action.ui.badge}
              text={key_insights.recommended_action.summary}
              impact={key_insights.recommended_action.expected_impact}
            />
          )}
        </div>
      </section>

      {/* ================= SEVERITY LEGEND ================= */}
      <SeverityLegend />
    </div>
  );
}

/* ===================================================== */
/* STYLES & COMPONENTS */
/* ===================================================== */

const severityStyles = {
  danger: {
    border: "border-l-red-500",
    bg: "from-rose-300/70 via-pink-200/60 to-red-300/70",
    pulse: true,
  },
  warning: {
    border: "border-l-amber-400",
    bg: "from-amber-300/70 via-yellow-200/60 to-amber-300/70",
  },
  success: {
    border: "border-l-emerald-400",
    bg: "from-emerald-300/70 via-teal-200/60 to-emerald-300/70",
  },
  info: {
    border: "border-l-sky-400",
    bg: "from-sky-200/70 via-blue-100/60 to-sky-200/70",
  },
};

function MainCard({ children, severity }) {
  const s = severityStyles[severity] || severityStyles.info;

  return (
    <div
      className={`
        relative rounded-xl border border-black/5 border-l-4 p-4 shadow-sm
        bg-gradient-to-br ${s.bg}
        transition-all duration-300 hover:scale-[1.01]
        ${s.border}
        ${s.pulse ? "animate-pulse-soft" : ""}
      `}
    >
      {children}
    </div>
  );
}

function ContextCard({ children, severity }) {
  const s = severityStyles[severity] || severityStyles.info;

  return (
    <div
      className={`
        rounded-xl border border-black/5 border-l-4 p-4 shadow-sm
        bg-gradient-to-br ${s.bg}
        ${s.border}
        transition-all duration-300 hover:scale-[1.02]
      `}
    >
      {children}
    </div>
  );
}

function InsightCard({ title, badge, text, impact, severity }) {
  const s = severityStyles[severity] || severityStyles.info;

  return (
    <div
      className={`
        rounded-xl border border-black/5 border-l-4 p-6 shadow-sm
        bg-gradient-to-br ${s.bg}
        ${s.border}
      `}
    >
      <div className="flex justify-between items-start">
        <h3 className="text-sm font-semibold text-slate-900">
          {title}
        </h3>
        <span className="text-[10px] font-medium text-slate-700">
          {badge}
        </span>
      </div>

      <p className="mt-3 text-sm text-slate-800 leading-relaxed">
        {text}
      </p>

      <p className="mt-4 text-xs text-slate-700">
        <span className="font-medium">Why this matters:</span>{" "}
        {impact}
      </p>
    </div>
  );
}

/* ================= TEXT ATOMS ================= */

function CardLabel({ children }) {
  return <p className="text-[11px] text-slate-700">{children}</p>;
}

function CardValue({ children }) {
  return <p className="mt-1 text-lg font-semibold text-slate-900">{children}</p>;
}

function CardSubtext({ children }) {
  return <p className="text-[11px] text-slate-700">{children}</p>;
}

function CardMeta({ children }) {
  return <p className="mt-2 text-[10px] text-slate-600">{children}</p>;
}

/* ================= SEVERITY LEGEND ================= */

function SeverityLegend() {
  return (
    <div className="fixed bottom-3 right-3 text-[10px] bg-white/70 backdrop-blur px-3 py-2 rounded-lg shadow">
      <div className="flex gap-3">
        <LegendDot color="bg-red-500" label="High" />
        <LegendDot color="bg-amber-400" label="Medium" />
        <LegendDot color="bg-emerald-400" label="Low" />
      </div>
    </div>
  );
}

function LegendDot({ color, label }) {
  return (
    <div className="flex items-center gap-1">
      <span className={`w-2 h-2 rounded-full ${color}`} />
      <span>{label}</span>
    </div>
  );
}

/* ================= BACKGROUND ================= */

