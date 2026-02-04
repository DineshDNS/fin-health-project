import pytest

from core.services.overview_assembler import build_overview_dto
from core.dto.enums import RiskLevel


# -------------------------------------------------
# Fixtures (mock engine outputs)
# -------------------------------------------------

@pytest.fixture
def analysis_data():
    return {
        "bank_analysis": {
            "net_cash_flow": -65000,
        },
        "gst_analysis": {
            "is_compliant": True,
        },
        "financial_analysis": {
            "financial_health_score": 40,
        },
    }


@pytest.fixture
def overview_logic():
    return {
        "financial_health_score": 40,
        "health_label": "WEAK",
        "credit_readiness": "LOW",
        "risk_level": "HIGH",
        "key_concerns": [
            {
                "type": "CASHFLOW",
                "severity": "HIGH",
                "message": "Negative cash flow detected",
            }
        ],
        "recommendations": [
            {
                "id": "CASHFLOW_001",
                "category": "CASHFLOW_IMPROVEMENT",
                "priority": "HIGH",
                "trigger": "Negative cash flow",
                "action": "Reduce expenses",
                "expected_impact": "Improves liquidity",
                "confidence": "HIGH",
                "ui": {
                    "badge": "High Priority",
                    "severity": "danger",
                    "icon": "trending-down",
                    "cta": {
                        "label": "Take Action",
                        "type": "primary",
                    },
                },
            }
        ],
        "eligible_products": [
            {
                "product_id": "NBFC_WC_001",
                "provider": "Partner NBFC",
                "product_type": "WORKING_CAPITAL",
                "linked_recommendation": "CASHFLOW_001",
                "confidence_score": 0.65,
                "confidence_label": "SUITABLE",
                "ui": {
                    "cta": {
                        "label": "Check Eligibility",
                        "type": "primary",
                    }
                },
            }
        ],
        "action_plan": [
            {
                "step": 1,
                "action": "Reduce expenses",
                "timeframe": "Next 30 days",
                "expected_outcome": "Improves cash surplus",
            }
        ],
        "ml_assessment": {
            "ml_risk_level": "HIGH",
            "confidence": 0.12,
        },
        "narrative": {
            "executive_summary": "High financial risk detected",
            "risk_explanation": {
                "explanation": "Based on cash flow and ML signals",
            },
            "confidence_note": "AI-assisted summary",
        },
    }


# -------------------------------------------------
# Core assembler tests
# -------------------------------------------------

def test_build_overview_dto_success(analysis_data, overview_logic):
    """
    GIVEN valid analysis + overview logic
    WHEN assembler is called
    THEN OverviewDTO should be built successfully
    """

    dto = build_overview_dto(
        business_id=1,
        industry="Retail",
        analysis=analysis_data,
        overview_logic=overview_logic,
    )

    assert dto.business_context.business_id == 1
    assert dto.business_context.data_availability.bank is True
    assert dto.health_summary.financial_health_score == 40
    assert dto.risk_summary.overall_risk_level == RiskLevel.HIGH
    assert len(dto.recommendations) == 1
    assert len(dto.products) == 1
    assert dto.ml_summary.confidence == 0.12


def test_partial_data_is_handled_gracefully(overview_logic):
    """
    GIVEN missing GST + financial data
    WHEN assembler is called
    THEN DTO should still be created
    """

    partial_analysis = {
        "bank_analysis": {
            "net_cash_flow": -50000,
        }
    }

    dto = build_overview_dto(
        business_id=2,
        industry="Retail",
        analysis=partial_analysis,
        overview_logic=overview_logic,
    )

    availability = dto.business_context.data_availability
    assert availability.bank is True
    assert availability.gst is False
    assert availability.financials is False


def test_invalid_ml_confidence_fails_fast(analysis_data, overview_logic):
    """
    GIVEN invalid ML confidence (>1)
    WHEN assembler builds DTO
    THEN validation error should be raised
    """

    overview_logic["ml_assessment"]["confidence"] = 1.8

    with pytest.raises(Exception):
        build_overview_dto(
            business_id=3,
            industry="Retail",
            analysis=analysis_data,
            overview_logic=overview_logic,
        )


def test_recommendation_mapping_integrity(analysis_data, overview_logic):
    """
    Ensure recommendation fields are mapped correctly
    """

    dto = build_overview_dto(
        business_id=4,
        industry="Retail",
        analysis=analysis_data,
        overview_logic=overview_logic,
    )

    rec = dto.recommendations[0]
    assert rec.id == "CASHFLOW_001"
    assert rec.priority.name == "HIGH"
    assert rec.ui.cta.label == "Take Action"


def test_product_mapping_integrity(analysis_data, overview_logic):
    """
    Ensure product fields are mapped correctly
    """

    dto = build_overview_dto(
        business_id=5,
        industry="Retail",
        analysis=analysis_data,
        overview_logic=overview_logic,
    )

    product = dto.products[0]
    assert product.product_id == "NBFC_WC_001"
    assert product.eligibility_score == 0.65
    assert product.ui.cta.label == "Check Eligibility"
