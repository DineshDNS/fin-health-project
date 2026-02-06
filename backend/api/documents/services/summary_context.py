from datetime import datetime


def build_documents_summary_context():
    """
    Builds raw domain context for documents summary.
    NO formatting, NO Response, NO UI logic.
    """

    return {
        "document_health": {
            "coverage_score": 78,
            "status": "PARTIAL",
            "freshness_days": 2,
            "required_documents": 8,
            "available_documents": 6,
            "ui_severity": "warning",
        },
        "documents": [
            {
                "document_id": "doc_001",
                "type": "BANK_STATEMENT",
                "period": {"year": 2025, "month": 12, "quarter": None},
                "source": "HDFC_BANK",
                "status": "PROCESSED",
                "uploaded_at": "2026-02-03T16:35:16.765156",
                "coverage_score": 92,
                "confidence": 0.95,
                "ui_severity": "success",
            },
            {
                "document_id": "doc_002",
                "type": "GST_RETURN",
                "period": {"year": 2025, "month": None, "quarter": "Q4"},
                "source": "GST_PORTAL",
                "status": "UPLOADED",
                "uploaded_at": "2026-02-01T16:35:16.765188",
                "coverage_score": 68,
                "confidence": 0.72,
                "ui_severity": "warning",
            },
        ],
        "coverage_map": {
            "liquidity": {"score": 90, "confidence": 0.88, "ui_severity": "success"},
            "cashflow": {"score": 85, "confidence": 0.92, "ui_severity": "success"},
            "profitability": {"score": 0, "confidence": 0.0, "ui_severity": "danger"},
            "compliance": {"score": 70, "confidence": 0.75, "ui_severity": "warning"},
        },
        "missing_documents": [
            {
                "type": "PROFIT_AND_LOSS",
                "required_for": ["profitability"],
                "missing_period": {"year": 2025, "month": None, "quarter": "Q4"},
                "reason": "No P&L uploaded for required period",
                "ui_severity": "danger",
            }
        ],
        "document_history": [
            {
                "document_id": "doc_001",
                "action": "REPLACED",
                "timestamp": "2026-02-04T16:35:16.765223",
                "replaced_by": "doc_003",
            }
        ],
        "last_sync": datetime.utcnow().isoformat(),
    }
