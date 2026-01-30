from django.urls import path
from .views import import_gst_data, import_bank_data

urlpatterns = [
    path("gst/import/", import_gst_data),
    path("bank/import/", import_bank_data),
]
