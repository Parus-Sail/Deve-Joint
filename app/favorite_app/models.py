from django.conf import settings
from django.db import models
from project_app.models import Project


class FavoriteBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE,
                             verbose_name="User")
    add_datetime = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Time added")

    class Meta:
        abstract = True


class FavoriteProjects(FavoriteBase):
    project = models.ForeignKey(Project,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                verbose_name="Project")

    class Meta:
        verbose_name = "Favorite project"
        verbose_name_plural = "Favorite projects"
