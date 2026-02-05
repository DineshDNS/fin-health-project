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
  if (isLoading) return null;

  const dto = data?.data ?? {};

  const financialHealth = {
    score: dto.financial_health?.overall_score ?? null,
    riskBand: dto.financial_health?.risk_band ?? "INFO",
    confidence: Math.round((dto.financial_health?.confidence ?? 0) * 100),
  };

  const healthBreakdown = dto.health_breakdown
    ? Object.entries(dto.health_breakdown).map(([key, v]) => ({
        label: key,
        score: v?.score ?? 0,
      }))
    : [];

  const riskFactors = dto.risk_factors ?? [];
  const impactSimulation = dto.impact_simulation ?? [];

  const ml = {
    confidence: Math.round((dto.ml_explainability?.confidence ?? 0) * 100),
    model_version: dto.ml_explainability?.model_version ?? "v1.0",
  };

  return (
    <div className="space-y-6">
      <FinancialHealthSummary financialHealth={financialHealth} />
      <HealthBreakdownCard healthBreakdown={healthBreakdown} />
      <RiskFactorsCard riskFactors={riskFactors} />
      <TrendSignalsCard trendSignals={dto.trend_signals} />
      <ImpactSimulationCard impactSimulation={impactSimulation} />
      <MLExplainabilityCard ml={ml} />
    </div>
  );
}
