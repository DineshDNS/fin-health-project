from django.urls import path
from api.overview import OverviewAPIView
from api.analysis import AnalysisAPIView
from api.documents import DocumentListAPIView

urlpatterns = [
    path("overview/", OverviewAPIView.as_view()),
    path("analysis/", AnalysisAPIView.as_view()),
    path("documents/", DocumentListAPIView.as_view()),
]
