
from django.db import models

class FinancialRecord(models.Model):
    company_name = models.CharField(max_length=200)
    revenue = models.FloatField()
    expenses = models.FloatField()
    assets = models.FloatField()
    liabilities = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class GSTRecord(models.Model):
    gstin = models.CharField(max_length=15)
    period = models.CharField(max_length=10)  # YYYY-MM
    total_sales = models.FloatField()
    total_tax_paid = models.FloatField()
    filing_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class BankStatement(models.Model):
    account_id = models.CharField(max_length=50)
    month = models.CharField(max_length=10)
    total_inflow = models.FloatField()
    total_outflow = models.FloatField()
    average_balance = models.FloatField()
    loan_emi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
