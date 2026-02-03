from django.db import models


def document_upload_path(instance, filename):
    """
    Store files by document type:
    media/documents/bank/
    media/documents/gst/
    media/documents/fin/
    """
    doc_type = instance.document_type.lower()
    return f"documents/{doc_type}/{filename}"


class Document(models.Model):
    DOCUMENT_TYPES = (
        ("BANK", "Bank Statement"),
        ("GST", "GST Document"),
        ("FIN", "Financial Document"),
    )

    FILE_FORMATS = (
        ("CSV", "CSV"),
        ("XLSX", "XLSX"),
        ("PDF", "PDF"),
    )

    file = models.FileField(upload_to=document_upload_path)
    file_format = models.CharField(max_length=10, choices=FILE_FORMATS)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} ({self.file_format})"
