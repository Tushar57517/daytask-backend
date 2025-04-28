from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email']

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class EmailChangeSerializer(serializers.ModelSerializer):
    new_email = serializers.EmailField(required=True)

    def validate_new_email(self, value):
        user = self.context['request'].user

class RequestEmailUpdateSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate_new_email(self, value):
        user = self.context['request'].user

        if value == user.email or User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        
        return value