from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Message

User = get_user_model()

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error":"user doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)