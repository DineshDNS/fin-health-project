from typing import List, Optional
from pydantic import BaseModel
from core.dto.enums import Severity, UISeverity


# ---------------------------------
# Business Context
# ---------------------------------

class DataAvailabilityDTO(BaseModel):
    bank: bool
    gst: bool
    financials: bool


class BusinessContextDTO(BaseModel):
    business_id: int
    industry: str
    data_availability: DataAvailabilityDTO
    last_updated: str


# ---------------------------------
# Health Summary
# ---------------------------------

class HealthSummaryUIDTO(BaseModel):
    severity: UISeverity


class HealthSummaryDTO(BaseModel):
    financial_health_score: int
    health_label: str
    credit_readiness: str
    ui: HealthSummaryUIDTO


# ---------------------------------
# Risk Summary
# ---------------------------------

class RiskSummaryUIDTO(BaseModel):
    severity: UISeverity


class RiskSummaryDTO(BaseModel):
    overall_risk_level: Severity
    risk_band: Severity
    confidence: float
    ui: RiskSummaryUIDTO


# ---------------------------------
# Key Insights (FINAL)
# ---------------------------------

class KeyInsightUIDTO(BaseModel):
    badge: str
    severity: UISeverity


class TopRiskInsightDTO(BaseModel):
    title: str
    severity: Severity
    summary: str
    why_it_matters: str
    ui: KeyInsightUIDTO


class RecommendedActionInsightDTO(BaseModel):
    title: str
    priority: Severity
    summary: str
    expected_impact: str
    ui: KeyInsightUIDTO


class KeyInsightsDTO(BaseModel):
    top_risk: TopRiskInsightDTO
    recommended_action: RecommendedActionInsightDTO


# ---------------------------------
# Immediate Attention Summary
# ---------------------------------

class AttentionSummaryUIDTO(BaseModel):
    severity: UISeverity


class AttentionSummaryDTO(BaseModel):
    title: str
    issue: str
    severity: Severity
    timeframe: str
    impact: str
    ui: AttentionSummaryUIDTO


# ---------------------------------
# FINAL Overview Response DTO
# ---------------------------------

class OverviewDataDTO(BaseModel):
    business_context: BusinessContextDTO
    health_summary: HealthSummaryDTO
    risk_summary: RiskSummaryDTO
    key_insights: KeyInsightsDTO
    attention_summary: AttentionSummaryDTO


class OverviewResponseDTO(BaseModel):
    request_id: str
    status: str
    data: OverviewDataDTO
    warnings: List[str] = []
    errors: List[str] = []
