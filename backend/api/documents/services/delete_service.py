from api.documents.models import Document, DocumentHistory
from analysis.models import DocumentAnalysis


class DocumentDeleteService:

    @staticmethod
    def delete(document_id):
        doc = Document.objects.get(id=document_id)

        # 🔥 DELETE ONLY THIS DOCUMENT'S ANALYSIS
        DocumentAnalysis.objects.filter(document=doc).delete()

        # Soft delete document
        doc.status = "DELETED"
        doc.save()

        # History entry
        DocumentHistory.objects.create(
            document=doc,
            action="DELETE"
        )

        return doc
