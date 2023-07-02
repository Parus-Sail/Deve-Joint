from django.db import models
from django.utils.translation import gettext_lazy as _

# TODO: нужно определить границы приложения main_app. Тогда можно будет написать модели и фикстуры,
#  а потом адаптировать под них вьюхи и шаблоны. Модель News создана для примера.


class MainappModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class MainappBaseModel(models.Model):
    objects = MainappModelManager()

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)
    deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

    def delete(self, *args):
        self.deleted = True
        self.save()

    def restore(self, *args):
        self.deleted = False
        self.save()

    class Meta:
        abstract = True


class NewsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(models.Model):
    objects = NewsManager()

    title = models.CharField(max_length=256, verbose_name='title')
    preamble = models.CharField(max_length=1024, blank=True, null=True, verbose_name='preamble')
    body = models.TextField(blank=False, null=False, verbose_name='body')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of creating',
        editable=False
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='date of editing',
        editable=False
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()
