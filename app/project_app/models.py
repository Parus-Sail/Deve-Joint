from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True,
                              blank=True,
                              related_name="owned_projects",
                              verbose_name=_("owner"),
                              on_delete=models.SET_NULL)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects",
                                     through="Membership", verbose_name=_("members"),
                                     through_fields=("project", "user"))

    def __repr__(self):
        return f'<Project: {self.title}>'

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("title",)


class Membership(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
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

    role = models.ForeignKey("role_app.Role",
                             null=False,
                             blank=False,
                             related_name="memberships",
                             on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Membership: {self.user} - {self.project} ({self.role})>'

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Membership")
        unique_together = (("project", "user"),)
