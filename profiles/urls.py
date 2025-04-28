from django.urls import path
from .views import GetUserProfileView, EditProfileNameView, RequestEmailUpdateView, ConfirmEmailUpdateView

urlpatterns = [
    path("me/", GetUserProfileView.as_view(), name="user-profile"),
    path("me/edit/name/", EditProfileNameView.as_view(), name="edit-user-profile-name"),
    path("me/edit/email/", RequestEmailUpdateView.as_view(), name="request-email-update"),
    path('me/edit/email/confirm/', ConfirmEmailUpdateView.as_view(), name='confirm-email-change')
]
