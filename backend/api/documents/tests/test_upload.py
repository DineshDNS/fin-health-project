from django.test import TestCase
from api.documents.services.upload_service import DocumentUploadService
from api.documents.dtos.upload_dto import DocumentUploadDTO

class TestUpload(TestCase):

    def test_upload_success(self):
        dto = DocumentUploadDTO(
            document_type="BANK_STATEMENT",
            year=2025,
            month=12,
            quarter=None,
            source="HDFC",
            filename="statement.pdf"
        )
        doc = DocumentUploadService.execute(dto)
        self.assertEqual(doc["type"], "BANK_STATEMENT")
