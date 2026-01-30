from django.urls import path
from .views import import_gst_data, import_bank_data, calculate_health

urlpatterns = [
    path("gst/import/", import_gst_data),
    path("bank/import/", import_bank_data),
    path("health/score/", calculate_health),
]
