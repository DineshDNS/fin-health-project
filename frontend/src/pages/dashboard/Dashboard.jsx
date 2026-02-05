import { useQuery } from "@tanstack/react-query";
import { fetchDashboard } from "../../services/dashboardService";

export default function Dashboard() {
  const {
    data,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["dashboard-overview"],
    queryFn: fetchDashboard,
  });

  if (isError) {
    return (
      <div className="rounded-xl bg-red-50 p-6 text-red-600">
        Failed to load dashboard. Please check API connection.
      </div>
    );
  }

  if (isLoading || !data) {
    return null; // skeletons already exist
  }

  const {
    last_updated,
    health_score,
    health_status,
    credit_status,
    risk_status,
    business,
    insights,
  } = data;

  return (
    <div className="space-y-12">
      {/* MAIN CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-2xl bg-rose-100 p-6">
          <h4>Health Score</h4>
          <div className="text-3xl font-bold">{health_score}</div>
          <div>{health_status}</div>
        </div>

        <div className="rounded-2xl bg-amber-100 p-6">
          <h4>Credit Readiness</h4>
          <div className="text-3xl font-bold">{credit_status}</div>
        </div>

        <div className="rounded-2xl bg-emerald-100 p-6">
          <h4>Overall Risk Level</h4>
          <div className="text-3xl font-bold">{risk_status}</div>
        </div>
      </div>

      {/* BUSINESS CONTEXT */}
      <div>
        <h3 className="mb-4">Business Context</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="rounded-xl bg-pink-50 p-4">
            Industry
            <div className="font-semibold">{business.industry}</div>
          </div>
          <div className="rounded-xl bg-pink-50 p-4">
            Bank Data
            <div className="font-semibold">
              {business.bank_data ? "Available" : "Unavailable"}
            </div>
          </div>
          <div className="rounded-xl bg-pink-50 p-4">
            GST Data
            <div className="font-semibold">
              {business.gst_data ? "Available" : "Unavailable"}
            </div>
          </div>
          <div className="rounded-xl bg-pink-50 p-4">
            Financial Data
            <div className="font-semibold">
              {business.financial_data ? "Available" : "Unavailable"}
            </div>
          </div>
        </div>
      </div>

      {/* KEY INSIGHTS */}
      <div>
        <h3 className="mb-4">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-2xl bg-white/40 backdrop-blur p-6">
            <h4>{insights[0]?.title ?? "Top Risk Identified"}</h4>
            <p className="mt-2">{insights[0]?.description}</p>
          </div>

          <div className="rounded-2xl bg-white/40 backdrop-blur p-6">
            <h4>Recommended Action</h4>
            <p className="mt-2">{insights[1]?.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
