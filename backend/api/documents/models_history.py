from django.db import models
import uuid


class DocumentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.CASCADE,
        related_name="history"
    )

    action = models.CharField(max_length=20)
    replaced_by = models.UUIDField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_history"
