from django.urls import path
from .views import signup
from .views import import_gst_data, import_bank_data, calculate_health,health_insights, cashflow_prediction
from .views import OverviewAPIView,FinancialUploadView, DocumentListAPIView, AnalysisAPIView
urlpatterns = [
    path("auth/signup/", signup),
    path("gst/import/", import_gst_data),
    path("bank/import/", import_bank_data),
    path("health/score/", calculate_health),
    path("health/insights/", health_insights),
    path("forecast/cashflow/", cashflow_prediction),

    path("upload/", FinancialUploadView.as_view()),
    path("overview/", OverviewAPIView.as_view()),
    path("documents/", DocumentListAPIView.as_view()),
    path("analysis/", AnalysisAPIView.as_view()),

]
