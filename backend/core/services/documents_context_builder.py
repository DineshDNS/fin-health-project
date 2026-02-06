import uuid
from datetime import datetime, timedelta
from core.services.documents_context import (
    DocumentsContext,
    DocumentContextItem,
    CoverageContextItem,
    MissingDocumentContextItem,
    DocumentHistoryContextItem,
)


def build_documents_context(user) -> DocumentsContext:
    """
    This is where:
    - DB queries happen
    - Rules run
    - ML confidence is attached
    """

    # --- MOCKED DATA FOR NOW (REAL IMPLEMENTATION LATER) ---

    documents = [
        DocumentContextItem(
            id="doc_001",
            type="BANK_STATEMENT",
            period={"year": 2025, "month": 12},
            source="HDFC_BANK",
            status="PROCESSED",
            uploaded_at=datetime.utcnow() - timedelta(days=2),
            coverage_score=92,
            confidence=0.95,
            severity="success",
        ),
        DocumentContextItem(
            id="doc_002",
            type="GST_RETURN",
            period={"year": 2025, "quarter": "Q4"},
            source="GST_PORTAL",
            status="UPLOADED",
            uploaded_at=datetime.utcnow() - timedelta(days=4),
            coverage_score=68,
            confidence=0.72,
            severity="warning",
        ),
    ]

    coverage_map = {
        "liquidity": CoverageContextItem(90, 0.88, "success"),
        "cashflow": CoverageContextItem(85, 0.92, "success"),
        "profitability": CoverageContextItem(0, 0.0, "danger"),
        "compliance": CoverageContextItem(70, 0.75, "warning"),
    }

    missing_documents = [
        MissingDocumentContextItem(
            type="PROFIT_AND_LOSS",
            required_for=["profitability"],
            period={"year": 2025, "quarter": "Q4"},
            reason="No P&L uploaded for required period",
            severity="danger",
        )
    ]

    history = [
        DocumentHistoryContextItem(
            document_id="doc_001",
            action="REPLACED",
            replaced_by="doc_003",
            timestamp=datetime.utcnow() - timedelta(days=1),
        )
    ]

    return DocumentsContext(
        request_id=str(uuid.uuid4()),
        coverage_score=78,
        coverage_status="PARTIAL",
        coverage_severity="warning",
        freshness_days=2,
        required_docs=8,
        available_docs=6,
        documents=documents,
        coverage_map=coverage_map,
        missing_documents=missing_documents,
        history=history,
        last_sync=datetime.utcnow(),
        warnings=[],
    )
