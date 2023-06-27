from django.urls import path
from django.views.generic import RedirectView

from .apps import MainpageappConfig
from .views import AboutPageView, ContactsPageView, JobsDetailView, JobsListingView, MainPageView

app_name = MainpageappConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="index")),
    path("index/", MainPageView.as_view(), name="index"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path("job-listing/", JobsListingView.as_view(), name="job-listing"),
    path("job-details/", JobsDetailView.as_view(), name="job-details"),
]
