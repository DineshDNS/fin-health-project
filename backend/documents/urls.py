from django.urls import path
from .views import UploadDocumentView, DocumentListView

urlpatterns = [
    path("upload/", UploadDocumentView.as_view()),
    path("documents/", DocumentListView.as_view()),
]
