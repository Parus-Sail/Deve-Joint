from django.urls import path
from favorite_app.views import FavoriteProjectsView, FavoriteProjectsAdd

app_name = 'favorite_app'

urlpatterns = [
    path('', FavoriteProjectsView.as_view(), name='favorite_projects_view'),
    path('add/<int:pk>/', FavoriteProjectsAdd.as_view(), name='favorite_projects_add'),
]
