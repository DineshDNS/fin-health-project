from django.test import TestCase
from api.documents.assembler.summary_assembler import DocumentsSummaryAssembler

class TestSummary(TestCase):

    def test_summary_structure(self):
        summary = DocumentsSummaryAssembler.build()
        self.assertIn("documents", summary)
        self.assertIn("document_history", summary)
