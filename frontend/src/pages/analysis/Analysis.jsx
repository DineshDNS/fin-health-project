import { useAnalysis } from "../../hooks/useAnalysis";
import AnalysisSkeleton from "./AnalysisSkeleton";

import FinancialHealthSummary from "./cards/FinancialHealthSummary";
import HealthBreakdownCard from "./cards/HealthBreakdownCard";
import RiskFactorsCard from "./cards/RiskFactorsCard";
import TrendSignalsCard from "./cards/TrendSignalsCard";
import ImpactSimulationCard from "./cards/ImpactSimulationCard";
import MLExplainabilityCard from "./cards/MLExplainabilityCard";

export default function Analysis() {
  const { data, isLoading } = useAnalysis();

  if (isLoading) return <AnalysisSkeleton />;

  const dto = data?.data ?? {};

  // ---------------- HEALTH ----------------
  const financialHealth = {
    score:
      dto.financial_health?.overall_score ??
      dto.financial_health_score ??
      0,

    riskBand:
      dto.financial_health?.risk_band ??
      dto.risk_level ??
      "INFO",

    confidence: Math.round(
      (dto.financial_health?.confidence ??
        dto.ml_explainability?.confidence ??
        0) * 100
    ),
  };

  // ---------------- BREAKDOWN ----------------
  const healthBreakdown = dto.health_breakdown
    ? Object.entries(dto.health_breakdown).map(([key, v]) => ({
        label: key,
        score: v?.score ?? 0,
      }))
    : [];

  // ---------------- RISKS ----------------
  const riskFactors = dto.risk_factors ?? [];

  // ---------------- TRENDS ----------------
  const trends = dto.trend_signals
    ? Object.entries(dto.trend_signals).map(([metric, value]) => ({
        metric: metric.replaceAll("_", " "),
        direction: value?.direction?.toLowerCase() || "flat",
        period: value?.period || "recent",
      }))
    : [];

  // ---------------- IMPACT ----------------
  const impactSimulation = dto.impact_simulation ?? [];

  // ---------------- ML ----------------
  const ml = {
    confidence: Math.round(
      (dto.ml_explainability?.confidence ?? 0) * 100
    ),
    model_version: dto.ml_explainability?.model_version ?? "v1.0",
  };

  // ---------------- AI INSIGHT ENGINE ----------------
  const generateInsight = () => {
    const highRisk = riskFactors.find(r => r.severity === "HIGH");
    if (highRisk) {
      return `${highRisk.type.replaceAll("_", " ")} risk detected with high severity.`;
    }

    const downTrend = trends.find(t => t.direction === "down");
    if (downTrend) {
      return `${downTrend.metric} showing a declining trend.`;
    }

    const upTrend = trends.find(t => t.direction === "up");
    if (upTrend) {
      return `${upTrend.metric} showing positive growth momentum.`;
    }

    if (financialHealth.score >= 70)
      return "Financial health is strong and stable.";

    if (financialHealth.score >= 40)
      return "Business stability is moderate with balanced indicators.";

    return "Financial instability signals detected. Immediate review advised.";
  };

  const aiInsight = generateInsight();

  return (
    <div className="space-y-8">
      <FinancialHealthSummary
        financialHealth={financialHealth}
        insight={aiInsight}
      />

      <HealthBreakdownCard healthBreakdown={healthBreakdown} />

      <RiskFactorsCard riskFactors={riskFactors} />

      <TrendSignalsCard trends={trends} />

      <ImpactSimulationCard impactSimulation={impactSimulation} />

      <MLExplainabilityCard ml={ml} />
    </div>
  );
}
