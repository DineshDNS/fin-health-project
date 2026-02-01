from django.urls import path
from .views import (
    SignupView,
    LoginView,
    UserProfileView,
    UpdateUserProfileView,
    ChangePasswordView,
)

urlpatterns = [
    # Auth
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),

    # Settings / Profile
    path("me/", UserProfileView.as_view()),
    path("update/", UpdateUserProfileView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]
