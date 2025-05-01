from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from decouple import config
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.contrib.auth import password_validation
from decouple import config

BASE_URL=config('BACKEND_BASE_URL')

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username','email','password']
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        token = RefreshToken.for_user(user).access_token
        verification_link = f"{BASE_URL}/api/accounts/verify-email/?token={str(token)}"

        send_mail(
                "Verify your Email",
                f"Click the link to verify your email: {verification_link}",
                config('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False
            )
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()

        if not user:
            raise serializers.ValidationError("user not found!")
        if not user.is_active:
            raise serializers.ValidationError("email not verified")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("incorrect password")
        
        return user
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Incorrect old password."})
        
        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "New password must be different from the old one."})

        password_validation.validate_password(new_password, user=user)
        return data
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("no account with this email found")
        return value
    
    def save(self):
          email = self.validated_data['email']
          user = User.objects.get(email=email)

          token = RefreshToken.for_user(user).access_token
          reset_link = f"{BASE_URL}/api/accounts/reset-password-confirm/?token={str(token)}"

          send_mail(
               "Reset Your Password",
               f"Click the link to reset your password: {reset_link}",
               config('EMAIL_HOST_USER'),
               [user.email],
               fail_silently=False
          )

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            access_token = AccessToken(data['token'])
            self.user_id = access_token['user_id']
        except Exception:
            raise serializers.ValidationError("Invalid or expired token.")
        return data

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.set_password(self.validated_data['new_password'])
        user.save()