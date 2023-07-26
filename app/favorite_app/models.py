from django.conf import settings
from django.db import models

from cv_app.models import CV
from project_app.models import Project
from vacancy_app.models import Vacancy


class FavoriteBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE,
                             verbose_name="User")
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Time added")

    class Meta:
        abstract = True


class FavoriteProjects(FavoriteBase):
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Project")

    class Meta:
        verbose_name = "Favorite project"
        verbose_name_plural = "Favorite projects"


class FavoriteVacancies(FavoriteBase):
    vacancy = models.ForeignKey(Vacancy, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Vacancy")

    class Meta:
        verbose_name = "Favorite vacancies"
        verbose_name_plural = "Favorite vacancies"


class FavoriteCVs(FavoriteBase):
    cv = models.ForeignKey(CV, null=False, blank=False, on_delete=models.CASCADE, verbose_name="CV")

    class Meta:
        verbose_name = "Favorite CV"
        verbose_name_plural = "Favorite CVs"
