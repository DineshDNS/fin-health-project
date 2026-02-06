from api.documents.models import Document, DocumentHistory
from analysis.models import DocumentAnalysis


class DocumentReplaceService:

    @staticmethod
    def replace(document_id, dto, file):
        old_doc = Document.objects.get(id=document_id)

        # 🔥 DELETE ONLY OLD DOCUMENT ANALYSIS
        DocumentAnalysis.objects.filter(document=old_doc).delete()

        # mark old as replaced
        old_doc.status = "REPLACED"
        old_doc.save()

        # create new document
        new_doc = Document.objects.create(
            type=dto["type"],
            year=dto["year"],
            month=dto.get("month"),
            quarter=dto.get("quarter"),
            source=dto.get("source"),
            file=file,
            status="UPLOADED"
        )

        # history entry
        DocumentHistory.objects.create(
            document=old_doc,
            action="REPLACE",
            replaced_by=new_doc.id
        )

        return new_doc
