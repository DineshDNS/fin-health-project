from django.contrib import admin
from .models import DocumentAnalysis


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document_type",
        "financial_health_score",
        "risk_level",
        "created_at",
    )

    list_filter = ("document_type", "risk_level")
    ordering = ("-created_at",)
