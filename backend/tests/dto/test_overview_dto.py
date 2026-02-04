import pytest

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


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def valid_ui(severity=SeverityLevel.info):
    return UIDecoration(
        badge="High Priority",
        severity=severity,
        icon="alert",
        cta=CTA(label="Take Action", type="primary"),
    )


# -------------------------------------------------
# Core DTO Validation
# -------------------------------------------------

def test_overview_dto_valid_payload():
    """
    GIVEN a fully valid overview payload
    WHEN OverviewDTO is created
    THEN validation should succeed
    """

    dto = OverviewDTO(
        business_context=BusinessContextDTO(
            business_id=1,
            industry="Retail",
            data_availability=DataAvailability(
                bank=True,
                gst=True,
                financials=True,
            ),
            last_updated="2026-02-03",
        ),
        health_summary=HealthSummaryDTO(
            financial_health_score=40,
            health_label="WEAK",
            credit_readiness="LOW",
            ui=valid_ui(SeverityLevel.danger),
        ),
        risk_summary=RiskSummaryDTO(
            overall_risk_level=RiskLevel.HIGH,
            key_risks=[
                RiskItemDTO(
                    type="CASHFLOW",
                    severity=RiskLevel.HIGH,
                    message="Negative cash flow detected",
                )
            ],
        ),
        recommendations=[
            RecommendationDTO(
                id="CASHFLOW_001",
                category="CASHFLOW_IMPROVEMENT",
                priority=PriorityLevel.HIGH,
                trigger="Negative cash flow",
                action="Reduce expenses",
                expected_impact="Improves liquidity",
                confidence=PriorityLevel.HIGH,
                ui=valid_ui(SeverityLevel.danger),
            )
        ],
        products=[
            ProductMatchDTO(
                product_id="NBFC_WC_001",
                provider="Partner NBFC",
                product_type="WORKING_CAPITAL",
                linked_recommendation_id="CASHFLOW_001",
                eligibility_score=0.65,
                eligibility_label="SUITABLE",
                ui=valid_ui(),
            )
        ],
        action_plan=[
            ActionPlanDTO(
                step=1,
                action="Reduce non-essential expenses",
                timeframe="Next 30 days",
                expected_outcome="Improves cash surplus",
            )
        ],
        ml_summary=MLSummaryDTO(
            risk_band=RiskLevel.HIGH,
            confidence=0.12,
            note="ML supports overall risk evaluation",
        ),
        narrative=NarrativeDTO(
            executive_summary="High financial risk detected",
            explanation="Based on cash flow and ML analysis",
            confidence_note="AI-assisted summary",
        ),
    )

    assert dto.business_context.business_id == 1
    assert dto.health_summary.financial_health_score == 40
    assert dto.risk_summary.overall_risk_level == RiskLevel.HIGH


# -------------------------------------------------
# Negative / Contract Safety Tests
# -------------------------------------------------

def test_missing_required_field_fails():
    """
    Missing required fields must fail validation
    """
    with pytest.raises(Exception):
        BusinessContextDTO(
            business_id=1,
            industry="Retail",
            # data_availability missing
            last_updated="2026-02-03",
        )


def test_invalid_risk_level_fails():
    """
    RiskLevel must be one of the enum values
    """
    with pytest.raises(Exception):
        RiskItemDTO(
            type="CASHFLOW",
            severity="CRITICAL",  # invalid
            message="Invalid risk level",
        )


def test_invalid_priority_fails():
    """
    Recommendation priority must be valid enum
    """
    with pytest.raises(Exception):
        RecommendationDTO(
            id="REC_001",
            category="COST",
            priority="URGENT",  # invalid
            trigger="High expenses",
            action="Reduce costs",
            expected_impact="Improves margin",
            confidence=PriorityLevel.HIGH,
            ui=valid_ui(),
        )


def test_ml_confidence_out_of_range_fails():
    """
    ML confidence should be a float between 0 and 1
    """
    with pytest.raises(Exception):
        MLSummaryDTO(
            risk_band=RiskLevel.HIGH,
            confidence=1.8,  # invalid
            note="Invalid confidence",
        )


# -------------------------------------------------
# Serialization Stability
# -------------------------------------------------

def test_overview_dto_serializes_to_dict():
    """
    DTO must serialize cleanly to dict (for API response)
    """
    dto = OverviewDTO(
        business_context=BusinessContextDTO(
            business_id=2,
            industry="Manufacturing",
            data_availability=DataAvailability(
                bank=True,
                gst=False,
                financials=True,
            ),
            last_updated="2026-02-03",
        ),
        health_summary=HealthSummaryDTO(
            financial_health_score=72,
            health_label="MODERATE",
            credit_readiness="MEDIUM",
            ui=valid_ui(),
        ),
        risk_summary=RiskSummaryDTO(
            overall_risk_level=RiskLevel.MODERATE,
            key_risks=[],
        ),
        recommendations=[],
        products=[],
        action_plan=[],
        ml_summary=MLSummaryDTO(
            risk_band=RiskLevel.MODERATE,
            confidence=0.55,
            note="Moderate ML risk",
        ),
        narrative=NarrativeDTO(
            executive_summary="Stable business",
            explanation="Healthy cash flow",
            confidence_note="AI-assisted summary",
        ),
    )

    data = dto.dict()
    assert isinstance(data, dict)
    assert "business_context" in data
    assert "health_summary" in data
