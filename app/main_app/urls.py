from django.urls import path
from django.views.generic import RedirectView

from .apps import MainAppConfig
from .views import (
    AboutPageView,
    ContactsPageView,
    MainPageView,
    NewsCreateView,
    NewsDeleteView,
    NewsDetailView,
    NewsListView,
    NewsUpdateView,
)

app_name = MainAppConfig.name

urlpatterns = [
    path("", RedirectView.as_view(url="index")),
    path("index/", MainPageView.as_view(), name="index"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<project_id>/detail', NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<project_id>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<project_id>/delete', NewsDeleteView.as_view(), name='news_delete'),
]
