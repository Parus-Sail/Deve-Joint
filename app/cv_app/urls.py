from django.urls import path
from django.views.generic import RedirectView

from . import views
from .apps import CvAppConfig

app_name = CvAppConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="list")),
    path("list/", views.CVListView.as_view(), name="list"),
    path("my-cv-list/", views.UserCVListView.as_view(), name="my-cv-list"),
    path("create/", views.CVCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CVDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.CVUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.CVDeleteView.as_view(), name="delete"),
]
