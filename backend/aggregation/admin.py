from django.contrib import admin
from .models import CumulativeAnalysisState

@admin.register(CumulativeAnalysisState)
class CumulativeAnalysisStateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "total_credits",
        "total_debits",
        "taxable_value",
        "financial_health_score",
        "updated_at",
    )
