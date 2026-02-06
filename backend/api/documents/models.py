from django.db import models
import uuid


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    quarter = models.CharField(max_length=2, null=True, blank=True)

    # UPDATED — made optional
    source = models.CharField(max_length=50, null=True, blank=True)

    file = models.FileField(upload_to="documents/")

    status = models.CharField(max_length=20, default="UPLOADED")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"


class DocumentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="history"
    )

    action = models.CharField(max_length=20)
    replaced_by = models.UUIDField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_history"
