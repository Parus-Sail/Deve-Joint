from django.contrib.auth import get_user_model
from django.db import models
from project_app.models import Project

User = get_user_model()


class Chat(models.Model):
    message = models.CharField(max_length=200)
    author = models.ForeignKey(User, blank=True, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, blank=True, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('-time',)