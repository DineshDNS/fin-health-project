from django.db import models
from django.contrib.auth.models import User


# =========================
# OPTIONAL (GLOBAL / ADMIN)
# =========================
class FinancialRecord(models.Model):
    company_name = models.CharField(max_length=200)
    revenue = models.FloatField()
    expenses = models.FloatField()
    assets = models.FloatField()
    liabilities = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# =========================
# USER-SCOPED MODELS
# =========================

class GSTRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    gstin = models.CharField(max_length=15)
    period = models.CharField(max_length=10)  # YYYY-MM
    total_sales = models.FloatField()
    total_tax_paid = models.FloatField()
    filing_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gstin} ({self.period})"


class BankStatement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    account_id = models.CharField(max_length=50)
    month = models.CharField(max_length=10)
    total_inflow = models.FloatField()
    total_outflow = models.FloatField()
    average_balance = models.FloatField()
    loan_emi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_id} ({self.month})"


class FinancialHealthScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    gst_record = models.ForeignKey(GSTRecord, on_delete=models.CASCADE)
    bank_record = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
    score = models.FloatField()
    risk_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"


class FinancialDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    file = models.FileField(upload_to="financial_docs/")
    file_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
