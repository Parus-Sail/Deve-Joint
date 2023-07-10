from django.apps import AppConfig


class ProjectAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_app'

    # def ready(self) -> None:
    #     # todo: выяснить нужно ли ипортировать тут модуль view?
    #     # from .views import ProjectDetailView
    #     return super().ready()
