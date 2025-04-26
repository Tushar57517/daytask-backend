from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer
)
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from django.core.mail import send_mail
from decouple import config

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"verification link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')

        try:
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])
            user.is_active = True
            user.save()
            return Response({"message":"email verified successfully"}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            return Response({"refresh":str(refresh), "access":str(refresh.access_token)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"message":"refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({"access":access_token}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context = {'request':request})

        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent to email"}, status=200)
        return Response(serializer.errors, status=400)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=200)
        return Response(serializer.errors, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"error":"refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"successfully logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user_email = user.email

        try:
            send_mail(
                    "Your account is deleted!",
                    f"Your request for deleting your account is successful. Your data is removed from our service.",
                    config('EMAIL_HOST_USER'),
                    [user_email],
                    fail_silently=False
                )
            user.delete()
            return Response({"message":"account deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception:
            return Response({"error":"something went wrong while deleting the account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)