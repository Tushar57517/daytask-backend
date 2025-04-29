from django.urls import path
from .views import TasksListView, TaskCreateView, TaskDetailView, TaskDeleteView, TaskUpdateView

urlpatterns = [
    path("list/", TasksListView.as_view(), name="tasks-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/detail/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
]
