from django.urls import path
from favorite_app.views import FavoriteProjectsAdd, FavoriteProjectsView, FavoriteProjectsRemove

app_name = 'favorite_app'

urlpatterns = [
    path('', FavoriteProjectsView.as_view(), name='favorite_projects_view'),
    path('add/<int:pk>/', FavoriteProjectsAdd.as_view(), name='favorite_projects_add'),
    path('remove/<int:pk>/', FavoriteProjectsRemove.as_view(), name='favorite_projects_remove'),
]