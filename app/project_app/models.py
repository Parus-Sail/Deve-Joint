from typing import Self

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey('Owner',
                              null=True,
                              related_name="own_projects",
                              verbose_name=_("owner"),
                              on_delete=models.SET_NULL)  # при удалении проекта не удаляем пользователя

    members = models.ManyToManyField(
        'Member',
        through='Membership',
        related_name='projects',
    )

    def __repr__(self):
        return f'<Project: {self.title}>'

    def get_absolute_url(self):
        return reverse_lazy('project_app:detail', kwargs={'project_id': self.pk})

    # def get_all_roles(self):
    #     return self.memberships.all()

    def save(self, *args, **kwargs) -> Self:
        if self.pk:
            #  При обновлени проекта — стандартное поведение
            super().save(*args, **kwargs)
        else:
            # При создании проекта — владелец становиться первым участником
            with transaction.atomic():
                super().save(*args, **kwargs)
                Membership.objects.create(user=self.owner, project=self, active=True)
        return self

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("title",)


class Membership(models.Model):

    user = models.ForeignKey('Member',
                             null=True,
                             blank=True,
                             default=None,
                             related_name="memberships",
                             on_delete=models.DO_NOTHING)

    project = models.ForeignKey("Project",
                                null=False,
                                blank=False,
                                related_name="memberships",
                                on_delete=models.CASCADE)

    active = models.BooleanField("Active", default=None)

    def __repr__(self):
        return f'<Membership: {self.user} - {self.project}>'

    def get_absolute_url(self):
        return reverse_lazy('project_app:members', kwargs={'project_id': self.project, 'member_id': self.id})

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Membership")
        unique_together = (("project", "user"),)


class Owner(User):

    def is_owner(self):
        pass

    def pass_project(self):
        pass

    class Meta:
        proxy = True


class Member(User):

    def is_member(self, project: Project) -> bool:
        """ Проверяет что пользователь является активным участником проекта """
        return self.objects.select_related('memberships').filter(memberships_project=project).exists(
            memberships_active=True)

    # filter(id=project.id).exists()

    def is_invited_to_project(self, project: Project) -> bool:
        return self.projectinvitation_set.filter(project=project).exists()

    def invite_to_project(self):
        pass

    def leave_project(self):
        pass

    class Meta:
        proxy = True
