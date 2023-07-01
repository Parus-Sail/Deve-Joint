from django.urls import path
from django.views.generic import RedirectView

from .apps import MainAppConfig
from .views import AboutPageView, ContactsPageView, MainPageView

app_name = MainAppConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="index")),
    path("index/", MainPageView.as_view(), name="index"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
]
