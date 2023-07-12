from django.urls import path

from . import views
from .apps import ProjectAppConfig

app_name = ProjectAppConfig.name

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    path('my_projects/', views.MyProjectsView.as_view(), name='my_projects'),
    path('search_results/', views.ProjectListView.as_view(), name='search_results'),
]

# path('<int:project_id>/include_member/', views.include_member_view, name='include_member'),
# path('<int:project_id>/exclude_member/', views.exclude_member_view, name='exclude_member'),
