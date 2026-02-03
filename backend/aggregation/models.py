from django.db import models

class CumulativeAnalysisState(models.Model):
    # BANK
    total_credits = models.FloatField(default=0)
    total_debits = models.FloatField(default=0)
    net_cash_flow = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)
    expense_ratio = models.FloatField(default=0)
    savings_ratio = models.FloatField(default=0)
    cashflow_volatile = models.BooleanField(default=False)

    # GST
    taxable_value = models.FloatField(default=0)
    gst_paid = models.FloatField(default=0)
    expected_gst = models.FloatField(default=0)
    payment_ratio = models.FloatField(default=0)
    compliance_gap = models.FloatField(default=0)
    is_compliant = models.BooleanField(default=False)

    # GLOBAL SCORE
    financial_health_score = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Cumulative Financial State"
