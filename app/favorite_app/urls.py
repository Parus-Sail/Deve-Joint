from django.urls import path
from favorite_app.views import (
    FavoriteProjectsAdd,
    FavoriteProjectsRemove,
    FavoritesView,
    FavoriteVacanciesAdd,
    FavoriteVacanciesRemove,
    FavoriteCVsAdd,
    FavoriteCVsRemove,
)

app_name = 'favorite_app'

urlpatterns = [
    path('', FavoritesView.as_view(), name='favorites_view'),
    path('projects/add/<int:pk>/', FavoriteProjectsAdd.as_view(), name='favorite_projects_add'),
    path('projects/remove/<int:pk>/', FavoriteProjectsRemove.as_view(), name='favorite_projects_remove'),
    path('vacancies/add/<int:pk>/', FavoriteVacanciesAdd.as_view(), name='favorite_vacancies_add'),
    path('vacancies/remove/<int:pk>/', FavoriteVacanciesRemove.as_view(), name='favorite_vacancies_remove'),
    path('cvs/add/<int:pk>/', FavoriteCVsAdd.as_view(), name='favorite_cvs_add'),
    path('cvs/remove/<int:pk>/', FavoriteCVsRemove.as_view(), name='favorite_cvs_remove'),
]
