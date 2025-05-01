from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer, UserNameSerializer, RequestEmailUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.mail import send_mail
from decouple import config
from rest_framework_simplejwt.exceptions import TokenError
from decouple import config

BASE_URL=config('BACKEND_BASE_URL')

User = get_user_model()

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EditProfileNameView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserNameSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user's name updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RequestEmailUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = RequestEmailUpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            new_email = serializer.validated_data['new_email']

            user = request.user
            user.pending_email = new_email
            user.save()

            token = RefreshToken.for_user(user).access_token

            confirm_url = f'{BASE_URL}/api/profile/me/edit/email/confirm/?token={str(token)}&email={str(new_email)}'

            send_mail(
                'Confirm your new email address',
                f'Click this link to confirm your email change: {confirm_url}',
                config('EMAIL_HOST_USER'),
                [new_email],
                fail_silently=False,
            )

            return Response({"message": "Confirmation email sent."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConfirmEmailUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        email = request.query_params.get('email')

        if not token or not email:
            return Response({"error": "Missing token or email."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.pending_email != email:
            return Response({"error": "No pending email match."}, status=status.HTTP_400_BAD_REQUEST)

        user.email = user.pending_email
        user.pending_email = None
        user.save()

        return Response({"message": "Email updated successfully."}, status=status.HTTP_200_OK)