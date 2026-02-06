from django.db import models
from api.documents.models import Document


class MLInference(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="ml_inferences"
    )

    model_name = models.CharField(max_length=100)
    model_version = models.CharField(max_length=50)

    # Snapshot of features used for prediction
    features = models.JSONField()

    # Prediction results
    probability = models.FloatField(null=True, blank=True)
    predicted_risk = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ml_inference"

    def __str__(self):
        return f"{self.model_name} | {self.predicted_risk}"
