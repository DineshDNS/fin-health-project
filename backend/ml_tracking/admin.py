from django.contrib import admin
from .models import MLInference


@admin.register(MLInference)
class MLInferenceAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "predicted_risk",
        "probability",
        "created_at",
    )
    readonly_fields = ("features",)
