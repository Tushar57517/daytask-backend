from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from django.core.mail import send_mail

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
        verification_link = f"http://localhost:8000/api/accounts/verify-email/?token={str(token)}"

        send_mail(
                "Verify your Email",
                f"Click the link to verify your email: {verification_link}",
                config('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False
            )
        
        return user