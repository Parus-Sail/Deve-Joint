from django.urls import path
from django.views.generic import RedirectView

from .apps import VacancyAppConfig
from .views import JobsDetailView, JobsListingView

app_name = VacancyAppConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="job-listing")),
    path("job-listing/", JobsListingView.as_view(), name="job-listing"),
    path("job-details/", JobsDetailView.as_view(), name="job-details"),
]
