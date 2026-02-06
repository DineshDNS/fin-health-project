from django.urls import path

from api.documents.views.summary import DocumentsSummaryView
from api.documents.views.upload import DocumentUploadView
from api.documents.views.replace import DocumentReplaceView
from api.documents.views.delete import DocumentDeleteView
from api.documents.views.history import DocumentHistoryView

urlpatterns = [
    path("summary/", DocumentsSummaryView.as_view()),
    path("upload/", DocumentUploadView.as_view()),
    path("replace/", DocumentReplaceView.as_view()),
    path("delete/", DocumentDeleteView.as_view()),
    path("history/<uuid:document_id>/", DocumentHistoryView.as_view()),
]
