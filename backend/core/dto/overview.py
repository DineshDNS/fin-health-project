from typing import List
from pydantic import BaseModel
from core.dto.enums import RiskLevel, SeverityLevel, PriorityLevel


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
    last_updated: str | None


# ---------------------------------
# Health Summary
# ---------------------------------

class HealthSummaryUIDTO(BaseModel):
    severity: SeverityLevel


class HealthSummaryDTO(BaseModel):
    financial_health_score: int
    health_label: str
    credit_readiness: str
    ui: HealthSummaryUIDTO


# ---------------------------------
# Risk Summary
# ---------------------------------

class RiskSummaryUIDTO(BaseModel):
    severity: SeverityLevel


class RiskSummaryDTO(BaseModel):
    overall_risk_level: RiskLevel
    risk_band: RiskLevel
    confidence: float
    ui: RiskSummaryUIDTO


# ---------------------------------
# Key Insights
# ---------------------------------

class KeyInsightUIDTO(BaseModel):
    badge: str
    severity: SeverityLevel


class TopRiskInsightDTO(BaseModel):
    title: str
    severity: RiskLevel
    summary: str
    why_it_matters: str
    ui: KeyInsightUIDTO


class RecommendedActionInsightDTO(BaseModel):
    title: str
    priority: PriorityLevel
    summary: str
    expected_impact: str
    ui: KeyInsightUIDTO


class KeyInsightsDTO(BaseModel):
    top_risk: TopRiskInsightDTO
    recommended_action: RecommendedActionInsightDTO


# ---------------------------------
# Attention Summary
# ---------------------------------

class AttentionSummaryUIDTO(BaseModel):
    severity: SeverityLevel


class AttentionSummaryDTO(BaseModel):
    title: str
    issue: str
    severity: RiskLevel
    timeframe: str
    impact: str
    ui: AttentionSummaryUIDTO


# ---------------------------------
# Final Overview Response
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
