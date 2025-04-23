from django.urls import path
from .views import (
    RegistetrView,
    VerifyEmailView,
    LoginView,
    RefreshTokenView,
    PasswordChangeView
)

urlpatterns = [
    path("register/", RegistetrView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
]
