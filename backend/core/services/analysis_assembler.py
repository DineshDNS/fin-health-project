from core.dto.analysis import (
    AnalysisDTO,
    FinancialHealthDTO,
    HealthBreakdownDTO,
    HealthPillarDTO,
    RiskFactorDTO,
    TrendSignalsDTO,
    MLExplainabilityDTO,
    ImpactSimulationDTO,
)
from core.dto.enums import RiskLevel, SeverityLevel


def build_analysis_dto(
    *,
    score: int,
    risk_level: RiskLevel,
    ml_result: dict,
    breakdown: dict,
    risks: list,
    trends: dict,
    impact_actions: list,
) -> AnalysisDTO:

    return AnalysisDTO(
        financial_health=FinancialHealthDTO(
            overall_score=score,
            risk_band=risk_level,
            confidence=ml_result.get("confidence", 0.0),
            ui={"severity": _severity_from_risk(risk_level)},
        ),

        health_breakdown=HealthBreakdownDTO(
            liquidity=_pillar(breakdown["liquidity"]),
            profitability=_pillar(breakdown["profitability"]),
            compliance=_pillar(breakdown["compliance"]),
            cashflow=_pillar(breakdown["cashflow"]),
        ),

        risk_factors=[
            RiskFactorDTO(
                type=r["type"],
                severity=r["severity"],
                confidence=r["confidence"],
                evidence=r["evidence"],
                ui={"severity": _severity_from_risk(r["severity"])},
            )
            for r in risks
        ],

        trend_signals=TrendSignalsDTO(
            cashflow_trend=trends["cashflow"],
            revenue_trend=trends["revenue"],
            expense_trend=trends["expense"],
            ui={"severity": SeverityLevel.warning},
        ),

        ml_explainability=MLExplainabilityDTO(
            risk_band=risk_level,
            confidence=ml_result.get("confidence", 0.0),
            key_features=ml_result.get("key_features", []),
            model_version=ml_result.get("model_version", "v1.0"),
        ),

        impact_simulation=[
            ImpactSimulationDTO(**item) for item in impact_actions
        ],
    )


# -----------------------------
# HELPERS
# -----------------------------

def _pillar(data: dict) -> HealthPillarDTO:
    return HealthPillarDTO(
        score=data["score"],
        status=data["status"],
        drivers=data.get("drivers", []),
        ui={"severity": _severity_from_score(data["score"])},
    )


def _severity_from_risk(risk: RiskLevel) -> SeverityLevel:
    if risk == RiskLevel.HIGH:
        return SeverityLevel.danger
    if risk == RiskLevel.MODERATE:
        return SeverityLevel.warning
    return SeverityLevel.info


def _severity_from_score(score: int) -> SeverityLevel:
    if score < 40:
        return SeverityLevel.danger
    if score < 70:
        return SeverityLevel.warning
    return SeverityLevel.info
