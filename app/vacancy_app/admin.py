from django.contrib import admin

from . import models as vacancy_models


@admin.register(vacancy_models.ApplicantLevel)
class ApplicantLevelAdmin(admin.ModelAdmin):
    list_display = ["name", "sort_order"]
    search_fields = [
        "name",
    ]


@admin.register(vacancy_models.EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "sort_order"]
    search_fields = [
        "name",
    ]


@admin.register(vacancy_models.JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "sort_order"]
    search_fields = ["name"]


@admin.register(vacancy_models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ["cv", "vacancy"]
    search_fields = ["cv"]
