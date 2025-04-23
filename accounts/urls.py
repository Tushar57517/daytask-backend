from django.urls import path
from .views import (
    RegistetrView,
    VerifyEmailView,
    LoginView,
    RefreshTokenView
)

urlpatterns = [
    path("register/", RegistetrView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
