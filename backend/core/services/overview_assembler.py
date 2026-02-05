from datetime import datetime, date
from typing import Dict, Any

from core.dto.overview import (
    OverviewDataDTO,
    OverviewResponseDTO,
    BusinessContextDTO,
    DataAvailabilityDTO,
    HealthSummaryDTO,
    HealthSummaryUIDTO,
    RiskSummaryDTO,
    RiskSummaryUIDTO,
    KeyInsightsDTO,
    TopRiskInsightDTO,
    RecommendedActionInsightDTO,
    KeyInsightUIDTO,
    AttentionSummaryDTO,
    AttentionSummaryUIDTO,
)

from core.dto.enums import RiskLevel, SeverityLevel, PriorityLevel


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _normalize_date(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    if value is None:
        return None
    return str(value)


def _risk_to_ui(risk: RiskLevel) -> SeverityLevel:
    if risk == RiskLevel.HIGH:
        return SeverityLevel.danger
    if risk == RiskLevel.MODERATE:
        return SeverityLevel.warning
    return SeverityLevel.info


def _priority_to_ui(priority: PriorityLevel) -> SeverityLevel:
    if priority == PriorityLevel.HIGH:
        return SeverityLevel.danger
    if priority == PriorityLevel.MEDIUM:
        return SeverityLevel.warning
    return SeverityLevel.info


# --------------------------------------------------
# Assembler (SINGLE SOURCE OF TRUTH)
# --------------------------------------------------

def build_overview_dto(
    *,
    business_id: int,
    industry: str,
    analysis: Dict[str, Any],
    overview_logic: Dict[str, Any],
) -> OverviewResponseDTO:

    # ---------------- Business Context ----------------
    data_availability = DataAvailabilityDTO(
        bank=bool(analysis.get("bank_analysis")),
        gst=bool(analysis.get("gst_analysis")),
        financials=bool(analysis.get("financial_analysis")),
    )

    business_context = BusinessContextDTO(
        business_id=business_id,
        industry=industry,
        data_availability=data_availability,
        last_updated=_normalize_date(
            analysis.get("last_updated")
            or analysis.get("bank_analysis", {}).get("created_at")
            or analysis.get("gst_analysis", {}).get("created_at")
            or analysis.get("financial_analysis", {}).get("created_at")
        ),
    )

    # ---------------- Health Summary ----------------
    risk_level = RiskLevel(overview_logic["risk_level"])

    health_summary = HealthSummaryDTO(
        financial_health_score=overview_logic["financial_health_score"],
        health_label=overview_logic["health_label"],
        credit_readiness=overview_logic["credit_readiness"],
        ui=HealthSummaryUIDTO(
            severity=_risk_to_ui(risk_level)
        ),
    )

    # ---------------- Risk Summary ----------------
    risk_summary = RiskSummaryDTO(
        overall_risk_level=risk_level,
        risk_band=risk_level,
        confidence=float(
            overview_logic.get("ml_assessment", {}).get("confidence", 0.0)
        ),
        ui=RiskSummaryUIDTO(
            severity=_risk_to_ui(risk_level)
        ),
    )

    # ---------------- Key Insights ----------------
    key_concerns = overview_logic.get("key_concerns", [])
    recommendations = overview_logic.get("recommendations", [])

    top_risk = None
    if key_concerns:
        kr = key_concerns[0]
        kr_severity = RiskLevel(kr["severity"])
        top_risk = TopRiskInsightDTO(
            title="Top Risk Identified",
            severity=kr_severity,
            summary=kr["message"],
            why_it_matters=(
                "May lead to short-term liquidity pressure "
                "and missed financial obligations."
            ),
            ui=KeyInsightUIDTO(
                badge=f"{kr_severity.value} Risk",
                severity=_risk_to_ui(kr_severity),
            ),
        )

    recommended_action = None
    if recommendations:
        rec = recommendations[0]
        priority = PriorityLevel(rec["priority"])
        recommended_action = RecommendedActionInsightDTO(
            title="Recommended Action",
            priority=priority,
            summary=rec["action"],
            expected_impact=rec["expected_impact"],
            ui=KeyInsightUIDTO(
                badge=f"{priority.value} Priority",
                severity=_priority_to_ui(priority),
            ),
        )

    key_insights = KeyInsightsDTO(
        top_risk=top_risk,
        recommended_action=recommended_action,
    )

    # ---------------- Attention Summary ----------------
    attention_summary = AttentionSummaryDTO(
        title="Immediate Attention Required",
        issue="Cash flow instability",
        severity=risk_level,
        timeframe="Next 30 days",
        impact="May affect payroll and vendor payments",
        ui=AttentionSummaryUIDTO(
            severity=_risk_to_ui(risk_level)
        ),
    )

    # ---------------- Final Data ----------------
    data = OverviewDataDTO(
        business_context=business_context,
        health_summary=health_summary,
        risk_summary=risk_summary,
        key_insights=key_insights,
        attention_summary=attention_summary,
    )

    return OverviewResponseDTO(
        request_id="",
        status="SUCCESS",
        data=data,
        warnings=[],
        errors=[],
    )
