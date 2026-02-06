from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class DocumentContextItem:
    id: str
    type: str
    period: dict
    source: str
    status: str
    uploaded_at: datetime
    coverage_score: int
    confidence: float
    severity: str


@dataclass
class CoverageContextItem:
    score: int
    confidence: float
    severity: str


@dataclass
class MissingDocumentContextItem:
    type: str
    required_for: List[str]
    period: dict
    reason: str
    severity: str


@dataclass
class DocumentHistoryContextItem:
    document_id: str
    action: str
    timestamp: datetime
    replaced_by: Optional[str] = None


@dataclass
class DocumentsContext:
    request_id: str

    # Summary
    coverage_score: int
    coverage_status: str
    coverage_severity: str
    freshness_days: int
    required_docs: int
    available_docs: int

    # Collections
    documents: List[DocumentContextItem]
    coverage_map: Dict[str, CoverageContextItem]
    missing_documents: List[MissingDocumentContextItem]
    history: List[DocumentHistoryContextItem]

    # Meta
    last_sync: datetime
    warnings: List[str]
