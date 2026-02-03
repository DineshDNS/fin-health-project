from django.db import models
from documents.models import Document


class DocumentAnalysis(models.Model):
    DOCUMENT_TYPES = (
        ("BANK", "Bank Statement"),
        ("GST", "GST Document"),
        ("FIN", "Financial Document"),
    )

    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPES
    )

    # ---------------- BANK METRICS ----------------
    total_credits = models.FloatField(default=0.0)
    total_debits = models.FloatField(default=0.0)
    net_cash_flow = models.FloatField(default=0.0)
    expense_ratio = models.FloatField(default=0.0)
    cashflow_volatile = models.BooleanField(default=False)

    # ---------------- GST METRICS ----------------
    taxable_value = models.FloatField(default=0.0)
    gst_paid = models.FloatField(default=0.0)
    expected_gst = models.FloatField(default=0.0)
    compliance_gap = models.FloatField(default=0.0)
    is_compliant = models.BooleanField(default=True)

    # ---------------- GLOBAL SCORE ----------------
    financial_health_score = models.IntegerField()
    risk_level = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} | Score: {self.financial_health_score}"
