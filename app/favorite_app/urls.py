from django.urls import path
from favorite_app.views import (
    FavoriteProjectsAdd,
    FavoriteProjectsRemove,
    FavoritesView,
    FavoriteVacanciesAdd,
    FavoriteVacanciesRemove,
)

app_name = 'favorite_app'

urlpatterns = [
    path('', FavoritesView.as_view(), name='favorites_view'),
    path('projects/add/<int:pk>/', FavoriteProjectsAdd.as_view(), name='favorite_projects_add'),
    path('projects/remove/<int:pk>/', FavoriteProjectsRemove.as_view(), name='favorite_projects_remove'),
    path('vacancies/add/<int:pk>/', FavoriteVacanciesAdd.as_view(), name='favorite_vacancies_add'),
    path('vacancies/remove/<int:pk>/', FavoriteVacanciesRemove.as_view(), name='favorite_vacancies_remove'),
]