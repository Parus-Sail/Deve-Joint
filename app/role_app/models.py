from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        "project_app.Project",
        null=True,
        blank=False,
        related_name="roles",
        verbose_name=_("project"),
        on_delete=models.CASCADE,
    )

    def __repr__(self) -> str:
        return f'<Role: {self.name}>'

    class Meta:
        verbose_name = _("Roles")
        verbose_name_plural = _("Role")
