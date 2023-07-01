from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name: str = "main_app/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "main_app/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "main_app/about.html"
