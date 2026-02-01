from django.urls import path
from .views import (
    SignupView,
    UserProfileView,
    UpdateUserProfileView,
    ChangePasswordView,
)

urlpatterns = [
    # Public
    path("signup/", SignupView.as_view(), name="signup"),

    # Protected
    path("me/", UserProfileView.as_view()),
    path("update/", UpdateUserProfileView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]
