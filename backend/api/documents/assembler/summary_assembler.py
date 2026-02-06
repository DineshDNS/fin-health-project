from api.documents.models import Document


class DocumentsSummaryAssembler:
    """
    Builds Documents Summary DTO for frontend
    """

    REQUIRED_TYPES = [
        "BANK_STATEMENT",
        "GST_RETURN",
        "BALANCE_SHEET",
        "PROFIT_AND_LOSS",   # 🔥 FIX: Added missing required type
    ]

    @staticmethod
    def build():
        # ONLY ACTIVE DOCUMENTS
        docs = Document.objects.filter(status="UPLOADED")

        coverage = {}
        present_types = set()

        for t in DocumentsSummaryAssembler.REQUIRED_TYPES:
            count = docs.filter(type=t).count()
            present = count > 0

            if present:
                present_types.add(t)

            coverage[t] = {
                "present": present,
                "count": count,
                "coverage_percent": 100 if present else 0,
            }

        missing = [
            t for t in DocumentsSummaryAssembler.REQUIRED_TYPES
            if t not in present_types
        ]

        total_required = len(DocumentsSummaryAssembler.REQUIRED_TYPES)

        if total_required == 0:
            health_score = 0
        else:
            health_score = int((len(present_types) / total_required) * 100)

        documents_list = [
            {
                "id": str(d.id),
                "type": d.type,
                "year": d.year,
                "month": d.month,
                "quarter": d.quarter,
                "source": d.source,
                "status": d.status,
                "uploaded_at": d.uploaded_at,
            }
            for d in docs.order_by("-uploaded_at")
        ]

        return {
            "documents": documents_list,
            "coverage_map": coverage,
            "missing_documents": missing,
            "health_score": health_score,
        }
