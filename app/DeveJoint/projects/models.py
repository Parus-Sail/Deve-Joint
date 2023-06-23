from datetime import timezone

from django.conf import settings
from django.db import models


class Membership(models.Model):
    # This model stores all project memberships. Also stores invitations to memberships that does not have assigned user.

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        default=None,
        related_name="memberships",
        on_delete=models.CASCADE,
    )

    role = models.ForeignKey(
        "users.Role",
        null=False,
        blank=False,
        related_name="memberships",
        on_delete=models.CASCADE,
    )

    project = models.ForeignKey(
        "Project",
        null=False,
        blank=False,
        related_name="memberships",
        on_delete=models.CASCADE,
    )

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ihaveinvited+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    is_admin = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="create at")

    class Meta:
        verbose_name = "membership"
        verbose_name_plural = "memberships"
        unique_together = ("user", "project")
        ordering = ["project"]


class Project(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name="name")
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=True, verbose_name="slug")
    description = models.TextField(null=False, blank=False, verbose_name="description")

    created_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(null=False, blank=False, verbose_name="created date", default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False, verbose_name="modified date")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="owned_projects",
        verbose_name="owner",
        on_delete=models.SET_NULL,
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        through="Membership",
        verbose_name=_("members"),
        through_fields=("project", "user"),
    )

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["name", "id"]
        index_together = [
            ["name", "id"],
        ]
