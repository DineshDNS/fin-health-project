from django.urls import path
from .analysis_view import AnalysisView
from .overview_view import OverviewView

urlpatterns = [
    path("analysis/", AnalysisView.as_view()),
    path("overview/", OverviewView.as_view()),
]
