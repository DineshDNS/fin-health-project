import { useEffect, useState } from "react";
import { getOverviewData } from "../api/overviewApi";

import HealthSummaryCard from "../components/overview/HealthSummaryCard";
import RiskAlerts from "../components/overview/RiskAlerts";
import ActionableInsights from "../components/overview/ActionableInsights";
import ProductRecommendations from "../components/overview/ProductRecommendations";

export default function Overview() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getOverviewData()
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        console.error(err);
        setError("No financial data found. Please upload documents.");
      });
  }, []);

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  if (!data) {
    return <p className="text-slate-600">Loading analysis...</p>;
  }

  return (
    <div className="min-h-full p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Financial Health Overview
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          AI-generated assessment based on uploaded financial data
        </p>
      </div>

      <HealthSummaryCard
        score={data.health_score ?? 0}
        riskLevel={data.risk_level ?? "UNKNOWN"}
      />

      <RiskAlerts riskFlags={data.risk_flags ?? []} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <ActionableInsights insights={data.actionable_insights ?? []} />
        <ProductRecommendations products={data.product_recommendations ?? []} />
      </div>
    </div>
  );
}
