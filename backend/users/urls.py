from django.urls import path
from .views import (
    SignupAPIView,
    UserProfileView,
    UpdateUserProfileView,
    ChangePasswordView,
)

urlpatterns = [
    # AUTH
    path("users/signup/", SignupAPIView.as_view(), name="signup"),

    # SETTINGS / PROFILE
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("update/", UpdateUserProfileView.as_view(), name="user-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
