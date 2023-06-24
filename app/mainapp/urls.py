from django.urls import path
from mainapp.apps import MainappConfig
from mainapp.views import IndexView

app_name = MainappConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
