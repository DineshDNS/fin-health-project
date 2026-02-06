from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class UISeverity(BaseModel):
    severity: str  # success | warning | danger


class DocumentPeriod(BaseModel):
    year: int
    month: Optional[int] = None
    quarter: Optional[str] = None


class DocumentItemDTO(BaseModel):
    document_id: str
    type: str
    period: DocumentPeriod
    source: str
    status: str
    uploaded_at: datetime
    coverage_score: int
    confidence: float
    ui: UISeverity


class CoverageDimensionDTO(BaseModel):
    score: int
    confidence: float
    ui: UISeverity


class MissingDocumentDTO(BaseModel):
    type: str
    required_for: List[str]
    missing_period: DocumentPeriod
    reason: str
    ui: UISeverity


class DocumentHistoryDTO(BaseModel):
    document_id: str
    action: str
    timestamp: datetime
    replaced_by: Optional[str] = None


class DocumentHealthDTO(BaseModel):
    coverage_score: int
    status: str
    freshness_days: int
    required_documents: int
    available_documents: int
    ui: UISeverity


class DocumentsSummaryDTO(BaseModel):
    document_health: DocumentHealthDTO
    documents: List[DocumentItemDTO]
    coverage_map: Dict[str, CoverageDimensionDTO]
    missing_documents: List[MissingDocumentDTO]
    document_history: List[DocumentHistoryDTO]
    last_sync: datetime
