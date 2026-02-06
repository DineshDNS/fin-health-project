from django.urls import path,include
from .analysis_view import AnalysisView
from .overview_view import OverviewView

urlpatterns = [

    path("overview/", OverviewView.as_view()),
    path("analysis/", AnalysisView.as_view()),

    
    path("documents/", include("api.documents.urls")),
    #path("analysis/", include("api.analysis.urls")),
]
