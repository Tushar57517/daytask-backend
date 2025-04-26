from django.urls import path
from .views import MessageListView

urlpatterns = [
    path("messages/<str:username>/", MessageListView.as_view(), name="messages"),
]
