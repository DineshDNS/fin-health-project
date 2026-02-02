import { useEffect, useState } from "react";
import { getOverviewData } from "../api/overviewApi";

import HealthSummaryCard from "../components/overview/HealthSummaryCard";
import RiskAlerts from "../components/overview/RiskAlerts";
import ActionableInsights from "../components/overview/ActionableInsights";
import ProductRecommendations from "../components/overview/ProductRecommendations";

export default function Overview() {
  const [overview, setOverview] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getOverviewData()
      .then((res) => {
        setOverview(res.data);
      })
      .catch((err) => {
        console.error(err);
        setError("No financial data available. Upload documents to begin.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-slate-600">
        Loading financial overview…
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-red-600 font-medium">
        {error}
      </div>
    );
  }

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Financial Health Overview
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          AI-generated assessment based on your uploaded financial data
        </p>
      </div>

      {/* Health Summary */}
      <HealthSummaryCard
        score={overview.financial_health_score ?? 0}
        riskLevel={overview.risk_level ?? "UNKNOWN"}
      />

      {/* Risk Alerts */}
      <div className="mt-6">
        <RiskAlerts riskFlags={overview.risk_alerts ?? []} />
      </div>

      {/* Insights + Products */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <ActionableInsights
          insights={overview.actionable_insights ?? []}
        />
        <ProductRecommendations
          products={overview.product_recommendations ?? []}
        />
      </div>
    </div>
  );
}
