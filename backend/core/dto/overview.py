from pydantic import BaseModel, confloat
from typing import List, Optional

from .enums import RiskLevel, PriorityLevel
from .ui import UIDecoration


# =========================
# Business Context
# =========================

class DataAvailability(BaseModel):
    bank: bool
    gst: bool
    financials: bool


class BusinessContextDTO(BaseModel):
    business_id: int
    industry: str
    data_availability: DataAvailability
    last_updated: str


# =========================
# Health Summary
# =========================

class HealthSummaryDTO(BaseModel):
    financial_health_score: int
    health_label: str        # STRONG | MODERATE | WEAK
    credit_readiness: str    # HIGH | MEDIUM | LOW
    ui: UIDecoration


# =========================
# Risk Summary
# =========================

class RiskItemDTO(BaseModel):
    type: str
    severity: RiskLevel
    message: str


class RiskSummaryDTO(BaseModel):
    overall_risk_level: RiskLevel
    key_risks: List[RiskItemDTO]


# =========================
# Recommendations
# =========================

class RecommendationDTO(BaseModel):
    id: str
    category: str
    priority: PriorityLevel
    trigger: str
    action: str
    expected_impact: str
    confidence: PriorityLevel
    ui: UIDecoration


# =========================
# Product Matching
# =========================

class ProductMatchDTO(BaseModel):
    product_id: str
    provider: str
    product_type: str
    linked_recommendation_id: Optional[str]
    eligibility_score: float
    eligibility_label: str
    ui: UIDecoration


# =========================
# Action Plan
# =========================

class ActionPlanDTO(BaseModel):
    step: int
    action: str
    timeframe: str
    expected_outcome: str


# =========================
# ML Summary (STRICT)
# =========================

class MLSummaryDTO(BaseModel):
    risk_band: RiskLevel
    confidence: confloat(ge=0.0, le=1.0)
    note: str


# =========================
# Narrative
# =========================

class NarrativeDTO(BaseModel):
    executive_summary: str
    explanation: str
    confidence_note: str


# =========================
# Final Overview DTO
# =========================

class OverviewDTO(BaseModel):
    business_context: BusinessContextDTO
    health_summary: HealthSummaryDTO
    risk_summary: RiskSummaryDTO
    recommendations: List[RecommendationDTO]
    products: List[ProductMatchDTO]
    action_plan: List[ActionPlanDTO]
    ml_summary: MLSummaryDTO
    narrative: NarrativeDTO
