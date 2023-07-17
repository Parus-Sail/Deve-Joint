from auth_app.models import BaseOpenSailUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

user_model: BaseOpenSailUser = get_user_model()


class VacancyAppBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)

    class Meta:
        abstract = True


class BusyType(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Busy type name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("BusyType")
        verbose_name_plural = _("BusyTypes")


class RelocationType(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Relocation name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("RelocationType")
        verbose_name_plural = _("RelocationTypes")


class CV(VacancyAppBaseModel):
    owner = models.ForeignKey(user_model, on_delete=models.DO_NOTHING)
    title = models.CharField(blank=False, max_length=256, verbose_name=_('Title'))
    salary = models.IntegerField(verbose_name=_('Salary'))
    technologies = models.CharField(max_length=1024, null=True, verbose_name=_('Technologies'))
    summary = models.TextField(blank=True, verbose_name=_('Summary'))
    education = models.TextField(verbose_name=_("Education"))
    experience = models.TextField(verbose_name=_("Experience"))
    busy_type = models.ForeignKey(BusyType, on_delete=models.DO_NOTHING)
    relocation = models.ForeignKey(RelocationType, on_delete=models.DO_NOTHING)
    is_published = models.BooleanField(default=False, null=False, verbose_name=_('Is published'))

    def __str__(self):
        return f'{self.owner.username}, #{self.id} - {self.title}'

    @property
    def owner_full_name(self):
        return ' '.join([self.owner.first_name.capitalize(), self.owner.last_name.capitalize()])

    def get_absolute_url(self):
        return reverse_lazy('cv_app:my-cv-list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("CV")
        verbose_name_plural = _("CVs")
        ordering = ['-created']
