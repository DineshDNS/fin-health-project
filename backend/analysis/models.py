from django.db import models


class DocumentAnalysis(models.Model):
    # ---------------- COMMON ----------------
    document = models.ForeignKey(
        "api.Document",   # ← FIXED HERE
        on_delete=models.CASCADE,
        related_name="analyses"
    )
    document_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    # ---------------- BANK ----------------
    total_credits = models.FloatField(null=True, blank=True)
    total_debits = models.FloatField(null=True, blank=True)
    net_cash_flow = models.FloatField(null=True, blank=True)
    expense_ratio = models.FloatField(null=True, blank=True)
    cashflow_volatile = models.BooleanField(default=False)

    # ---------------- GST ----------------
    taxable_value = models.FloatField(null=True, blank=True)
    gst_paid = models.FloatField(null=True, blank=True)
    expected_gst = models.FloatField(null=True, blank=True)
    compliance_gap = models.FloatField(null=True, blank=True)
    is_compliant = models.BooleanField(default=True)

    # ---------------- FIN (NEW) ----------------
    total_assets = models.FloatField(null=True, blank=True)
    total_liabilities = models.FloatField(null=True, blank=True)
    savings_ratio = models.FloatField(null=True, blank=True)
    current_ratio = models.FloatField(null=True, blank=True)

    # ---------------- SCORES ----------------
    financial_health_score = models.FloatField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, null=True, blank=True)
