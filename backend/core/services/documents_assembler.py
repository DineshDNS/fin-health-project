from datetime import datetime
from core.dto.documents import (
    DocumentsSummaryDTO,
    DocumentHealthDTO,
    DocumentItemDTO,
    CoverageDimensionDTO,
    MissingDocumentDTO,
    DocumentHistoryDTO,
    UISeverity,
    DocumentPeriod,
)


class DocumentsAssembler:
    @staticmethod
    def build(context) -> DocumentsSummaryDTO:
        return DocumentsSummaryDTO(
            document_health=DocumentHealthDTO(
                coverage_score=context.coverage_score,
                status=context.coverage_status,
                freshness_days=context.freshness_days,
                required_documents=context.required_docs,
                available_documents=context.available_docs,
                ui=UISeverity(severity=context.coverage_severity),
            ),
            documents=[
                DocumentItemDTO(
                    document_id=d.id,
                    type=d.type,
                    period=DocumentPeriod(**d.period),
                    source=d.source,
                    status=d.status,
                    uploaded_at=d.uploaded_at,
                    coverage_score=d.coverage_score,
                    confidence=d.confidence,
                    ui=UISeverity(severity=d.severity),
                )
                for d in context.documents
            ],
            coverage_map={
                k: CoverageDimensionDTO(
                    score=v.score,
                    confidence=v.confidence,
                    ui=UISeverity(severity=v.severity),
                )
                for k, v in context.coverage_map.items()
            },
            missing_documents=[
                MissingDocumentDTO(
                    type=m.type,
                    required_for=m.required_for,
                    missing_period=DocumentPeriod(**m.period),
                    reason=m.reason,
                    ui=UISeverity(severity=m.severity),
                )
                for m in context.missing_documents
            ],
            document_history=[
                DocumentHistoryDTO(
                    document_id=h.document_id,
                    action=h.action,
                    timestamp=h.timestamp,
                    replaced_by=h.replaced_by,
                )
                for h in context.history
            ],
            last_sync=context.last_sync or datetime.utcnow(),
        )
