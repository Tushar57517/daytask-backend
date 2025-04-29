from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    members = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)

    def __str__(self):
        return self.title    