from typing import List
from pydantic import BaseModel
from core.dto.enums import SeverityLevel, RiskLevel


# -----------------------------
# FINANCIAL HEALTH (TOP)
# -----------------------------

class FinancialHealthDTO(BaseModel):
    overall_score: int
    risk_band: RiskLevel
    confidence: float
    ui: dict


# -----------------------------
# HEALTH BREAKDOWN
# -----------------------------

class HealthPillarDTO(BaseModel):
    score: int
    status: str
    drivers: List[str]
    ui: dict


class HealthBreakdownDTO(BaseModel):
    liquidity: HealthPillarDTO
    profitability: HealthPillarDTO
    compliance: HealthPillarDTO
    cashflow: HealthPillarDTO


# -----------------------------
# RISK FACTORS
# -----------------------------

class RiskFactorDTO(BaseModel):
    type: str
    severity: RiskLevel
    confidence: float
    evidence: List[str]
    ui: dict


# -----------------------------
# TREND SIGNALS
# -----------------------------

class TrendSignalsDTO(BaseModel):
    cashflow_trend: str
    revenue_trend: str
    expense_trend: str
    ui: dict


# -----------------------------
# ML EXPLAINABILITY
# -----------------------------

class MLExplainabilityDTO(BaseModel):
    risk_band: RiskLevel
    confidence: float
    key_features: List[str]
    model_version: str


# -----------------------------
# IMPACT SIMULATION
# -----------------------------

class ImpactSimulationDTO(BaseModel):
    action: str
    timeframe: str
    expected_outcome: str


# -----------------------------
# ANALYSIS ROOT DTO
# -----------------------------

class AnalysisDTO(BaseModel):
    financial_health: FinancialHealthDTO
    health_breakdown: HealthBreakdownDTO
    risk_factors: List[RiskFactorDTO]
    trend_signals: TrendSignalsDTO
    ml_explainability: MLExplainabilityDTO
    impact_simulation: List[ImpactSimulationDTO]
