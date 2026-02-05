from django.urls import path
from .analysis_view import AnalysisView
from .overview_view import OverviewView

urlpatterns = [

    path("overview/", OverviewView.as_view()),
    path("analysis/", AnalysisView.as_view())
]
