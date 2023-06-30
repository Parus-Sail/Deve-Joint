from django.urls import path

from . import views

app_name = 'projectapp'

urlpatterns = [
    path('', views.list_projects_view, name='list_projects'),
    path('create/', views.create_project_view, name='create_project'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/update/', views.update_project_view, name='update_project'),
    path('<int:project_id>/delete/', views.delete_project_view, name='delete_project'),
    path('<int:project_id>/include_member/', views.include_member_view, name='include_member'),
    path('<int:project_id>/exclude_member/', views.exclude_member_view, name='exclude_member'),
]
