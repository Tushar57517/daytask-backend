from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q

class TasksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        tasks = Task.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"task created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"setail":"task not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user

        if task.owner != user and user not in task.members.all():
            return Response(
                {"detail": "You do not have permission to view this task."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
class TaskDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"message": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if task.owner != user:
            return Response(
                {"message": "You do not have permission to delete this task."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.delete()
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"message": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if task.owner != user:
            return Response(
                {"message": "You do not have permission to update this task."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)