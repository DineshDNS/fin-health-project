from django.urls import path
from .upload import UploadDocumentView
from .documents import DocumentsListView, DeleteDocumentView

urlpatterns = [
    path("upload/", UploadDocumentView.as_view()),
    path("documents/", DocumentsListView.as_view()),
    path("documents/<int:pk>/", DeleteDocumentView.as_view()),
]
