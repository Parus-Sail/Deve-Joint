from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(User,
                              null=True,
                              related_name="projects",
                              verbose_name=_("owner"),
                              on_delete=models.SET_NULL)  # при удалении проекта не удаляем пользователя

    # def __repr__(self):
    # return f'<Project: {self.title}>'

    def get_absolute_url(self):
        return reverse_lazy('project_app:detail', kwargs={'project_id': self.pk})

    def get_all_roles(self):
        return self.memberships.all()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("title",)


class Membership(models.Model):

    user = models.ForeignKey(User,
                             null=True,
                             blank=True,
                             default=None,
                             related_name="memberships",
                             on_delete=models.CASCADE)

    project = models.ForeignKey("Project",
                                null=False,
                                blank=False,
                                related_name="memberships",
                                on_delete=models.CASCADE)

    waiting_status = models.CharField(
        max_length=10,
        default=None,
        blank=True,
        null=True,
        choices=[
            ('wait_user', 'invited'),  # ждем решение от потенциального участника
            ('wait_owner', 'applicated'),  # ждем решение от владельца проекта
        ],
    )

    def __repr__(self):
        return f'<Membership: {self.user} - {self.project}>'

    def get_absolute_url(self):
        return reverse_lazy('project_app:members', kwargs={'project_id': self.project, 'member_id': self.id})

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Membership")
        unique_together = (("project", "user"),)
