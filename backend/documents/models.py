from django.db import models
from django.contrib.auth.models import User


class FinancialDocument(models.Model):
    CATEGORY_CHOICES = [
        ("FIN", "Financial Statement"),
        ("BANK", "Bank Statement"),
        ("GST", "GST Return"),
    ]

    FILE_TYPES = [
        ("PDF", "PDF"),
        ("CSV", "CSV"),
        ("XLSX", "XLSX"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to="financial_documents/")
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    document_type = models.CharField(max_length=20)

    period_from = models.DateField(null=True, blank=True)
    period_to = models.DateField(null=True, blank=True)

    source = models.CharField(max_length=100, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 🔑 processing status
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.document_type}"

class DocumentParseResult(models.Model):
    document = models.OneToOneField(
        FinancialDocument,
        on_delete=models.CASCADE,
        related_name="parse_result"
    )

    rows = models.IntegerField(null=True, blank=True)
    columns = models.JSONField(null=True, blank=True)
    text_length = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
