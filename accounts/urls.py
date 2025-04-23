from django.urls import path
from .views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    RefreshTokenView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetRequestView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
    path('reset-password/', PasswordResetRequestView.as_view(), name="reset-password"),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
]
