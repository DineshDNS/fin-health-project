from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

uploaded_at = models.DateTimeField(default=timezone.now)

from django.utils import timezone

uploaded_at = models.DateField(default=timezone.now)



class FinancialDocument(models.Model):
    CATEGORY_CHOICES = [
        ("FIN", "Financial Statement"),
        ("BANK", "Bank Statement"),
        ("GST", "GST Return"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to="financial_documents/")

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    document_type = models.CharField(max_length=20)

    period_from = models.DateField()
    period_to = models.DateField()

    source = models.CharField(max_length=100, blank=True)

    file_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.document_type}"
