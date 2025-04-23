from django.urls import path
from .views import (
    RegistetrView,
    VerifyEmailView
)

urlpatterns = [
    path("register/", RegistetrView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
