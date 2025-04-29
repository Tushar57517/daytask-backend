from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    members_detail = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'desc', 'time', 'date', 'created_at', 'updated_at', 'owner', 'members', 'members_detail']

    def get_members_detail(self, obj):
        return [user.username for user in obj.members.all()]
    
    def validate_members(self, value):
        users = []
        for username in value:
            try:
                user = User.objects.get(username=username)
                users.append(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"Invalid username: {username}")
        return users
    
    def create(self, validated_data):
        member_usernames = validated_data.pop('members', [])
        task = Task.objects.create(owner=self.context['request'].user, **validated_data)
        users = User.objects.filter(username__in=member_usernames)
        task.members.set(users)
        return task
    
    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if members is not None:
            instance.members.set(members)
        return instance
