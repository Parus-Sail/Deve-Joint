from django.urls import path

from . import views
from .apps import ProjectAppConfig

app_name = ProjectAppConfig.name

urlpatterns = [
    # ============================================= PROJECTS =================================================
    path('', views.ProjectListView.as_view(), name='list'),
    path('<int:project_id>/', views.ProjectDetailView.as_view(), name='detail'),
    # ============================================= OWN PROJECTS =============================================
    path('my_projects/', views.OwnProjectListView.as_view(), name='my_project_list'),
    path('<int:project_id>/my_project/', views.OwnProjectDetail.as_view(), name='my_project'),
    path('create/', views.OwnProjectCreateView.as_view(), name='create'),
    path('<int:project_id>/update/', views.OwnProjectUpdateView.as_view(), name='update'),
    path('<int:project_id>/delete/', views.OwnProjectDeleteView.as_view(), name='delete'),
]

# ============================================= MEMBERS ==================================================
# path('<int:project_id>/pass_ownership/', views.OwnProjectUpdateView.as_view(), name='pass_ownership'),  # todo
# path('<int:project_id>/members/', views.ListProjectMembersView.as_view(), name='members'),
# # приглашение от участника # todo скорректировать путь в случае необходимости
# path('profile/<int:user_id>/invite/<int:project_id>/', views.InviteToProjectView.as_view(), name='invite'),
# path('my_profile/invites/<int:project_id>/approve/', views.ApproveMemberView.as_view(), name='approve'),
# path('my_profile/invites/<int:project_id>/disapprove/', views.DisapproveMemberView.as_view(), name='disapprove'),
# # заявление от желающего вступить
# path('<int:project_id>/application/', views.ApplicationMemberView.as_view(), name='application'),
# path('<int:project_id>/members/<int:applicant_id>/accept/', views.AcceptMemberView.as_view(), name='accept'),
# path('<int:project_id>/members/<int:applicant_id>/reject/', views.RejectMemberView.as_view(), name='reject'),
# path('<int:project_id>/include_member/', views.include_member_view, name='include_member'),
# path('<int:project_id>/exclude_member/', views.exclude_member_view, name='exclude_member'),
