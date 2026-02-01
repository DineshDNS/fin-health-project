from django.urls import path
from .views import OverviewView, AnalysisMetricsView

urlpatterns = [
    path("overview/", OverviewView.as_view()),
     path("metrics/", AnalysisMetricsView.as_view()),
]
