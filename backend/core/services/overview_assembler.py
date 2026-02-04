from datetime import date
from typing import Dict, Any

from core.dto.overview import (
    OverviewDTO,
    BusinessContextDTO,
    DataAvailability,
    HealthSummaryDTO,
    RiskSummaryDTO,
    RiskItemDTO,
    RecommendationDTO,
    ProductMatchDTO,
    ActionPlanDTO,
    MLSummaryDTO,
    NarrativeDTO,
)
from core.dto.ui import UIDecoration, CTA
from core.dto.enums import RiskLevel, PriorityLevel, SeverityLevel


def build_overview_dto(
    *,
    business_id: int,
    industry: str,
    analysis: Dict[str, Any],
    overview_logic: Dict[str, Any],
) -> OverviewDTO:
    """
    Assemble the UX-safe OverviewDTO for /api/overview.

    This is the ONLY place where:
    - raw analysis
    - rule-based decisions
    - ML outputs
    are normalized into a frontend-safe contract.
    """

    # -------------------------------------------------
    # Business Context
    # -------------------------------------------------
    business_context = BusinessContextDTO(
        business_id=business_id,
        industry=industry,
        data_availability=DataAvailability(
            bank="bank_analysis" in analysis,
            gst="gst_analysis" in analysis,
            financials="financial_analysis" in analysis,
        ),
        last_updated=str(date.today()),
    )

    # -------------------------------------------------
    # Health Summary
    # -------------------------------------------------
    health_summary = HealthSummaryDTO(
        financial_health_score=overview_logic["financial_health_score"],
        health_label=overview_logic["health_label"],
        credit_readiness=overview_logic["credit_readiness"],
        ui=UIDecoration(
            badge=None,
            severity=(
                SeverityLevel.danger
                if overview_logic["risk_level"] == "HIGH"
                else SeverityLevel.warning
                if overview_logic["risk_level"] == "MODERATE"
                else SeverityLevel.info
            ),
            icon="alert-octagon",
        ),
    )

    # -------------------------------------------------
    # Risk Summary
    # -------------------------------------------------
    risk_summary = RiskSummaryDTO(
        overall_risk_level=RiskLevel[overview_logic["risk_level"]],
        key_risks=[
            RiskItemDTO(
                type=item["type"],
                severity=RiskLevel[item["severity"]],
                message=item["message"],
            )
            for item in overview_logic.get("key_concerns", [])
        ],
    )

    # -------------------------------------------------
    # Recommendations
    # -------------------------------------------------
    recommendations = []
    for rec in overview_logic.get("recommendations", []):
        recommendations.append(
            RecommendationDTO(
                id=rec["id"],
                category=rec["category"],
                priority=PriorityLevel[rec["priority"]],
                trigger=rec["trigger"],
                action=rec["action"],
                expected_impact=rec["expected_impact"],
                confidence=PriorityLevel[rec["confidence"]],
                ui=UIDecoration(
                    badge=rec["ui"].get("badge"),
                    severity=SeverityLevel[rec["ui"]["severity"]],
                    icon=rec["ui"]["icon"],
                    cta=CTA(**rec["ui"]["cta"]) if rec["ui"].get("cta") else None,
                ),
            )
        )

    # -------------------------------------------------
    # Product Matching
    # -------------------------------------------------
    products = []
    for prod in overview_logic.get("eligible_products", []):
        products.append(
            ProductMatchDTO(
                product_id=prod["product_id"],
                provider=prod["provider"],
                product_type=prod["product_type"],
                linked_recommendation_id=prod.get("linked_recommendation"),
                eligibility_score=prod["confidence_score"],
                eligibility_label=prod["confidence_label"],
                ui=UIDecoration(
                    badge=None,
                    severity=SeverityLevel.info,
                    icon="bank",
                    cta=CTA(**prod["ui"]["cta"]) if prod["ui"].get("cta") else None,
                ),
            )
        )

    # -------------------------------------------------
    # Action Plan
    # -------------------------------------------------
    action_plan = [
        ActionPlanDTO(
            step=step["step"],
            action=step["action"],
            timeframe=step["timeframe"],
            expected_outcome=step["expected_outcome"],
        )
        for step in overview_logic.get("action_plan", [])
    ]

    # -------------------------------------------------
    # ML Summary (SAFE & DEFENSIVE)
    # -------------------------------------------------
    ml_assessment = overview_logic.get("ml_assessment")

    if isinstance(ml_assessment, dict):
        ml_risk_level = ml_assessment.get(
            "ml_risk_level", overview_logic["risk_level"]
        )
        ml_confidence = ml_assessment.get("confidence", 0.0)
    else:
        # ML unavailable / failed / not applicable
        ml_risk_level = overview_logic["risk_level"]
        ml_confidence = 0.0

    ml_summary = MLSummaryDTO(
        risk_band=RiskLevel[ml_risk_level],
        confidence=ml_confidence,
        note="ML assessment supports overall risk evaluation",
    )

    # -------------------------------------------------
    # Narrative
    # -------------------------------------------------
    narrative = NarrativeDTO(
        executive_summary=overview_logic["narrative"]["executive_summary"],
        explanation=overview_logic["narrative"]["risk_explanation"]["explanation"],
        confidence_note=overview_logic["narrative"]["confidence_note"],
    )

    # -------------------------------------------------
    # Final Overview DTO
    # -------------------------------------------------
    return OverviewDTO(
        business_context=business_context,
        health_summary=health_summary,
        risk_summary=risk_summary,
        recommendations=recommendations,
        products=products,
        action_plan=action_plan,
        ml_summary=ml_summary,
        narrative=narrative,
    )
