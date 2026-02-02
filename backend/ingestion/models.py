from django.db import models
from django.contrib.auth.models import User


class IngestedDocument(models.Model):
    CATEGORY_CHOICES = (
        ("FIN", "Financial Statement"),
        ("BANK", "Bank Statement"),
        ("GST", "GST Return"),
    )

    DOCUMENT_TYPE_CHOICES = (
        ("PL", "Profit & Loss"),
        ("BS", "Balance Sheet"),
        ("CF", "Cash Flow"),
        ("BANK", "Bank Statement"),
        ("GSTR1", "GSTR-1"),
        ("GSTR3B", "GSTR-3B"),
    )

    DETECTED_TYPES = (
        ("BANK", "Bank Statement"),
        ("GST", "GST Return"),
        ("PDF", "PDF"),
        ("UNKNOWN", "Unknown"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")

    # 👇 USER SELECTED
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)

    # 👇 SYSTEM DETECTED
    detected_type = models.CharField(
        max_length=20,
        choices=DETECTED_TYPES,
        default="UNKNOWN",
    )

    parsed_data = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
