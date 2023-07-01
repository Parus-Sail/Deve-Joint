from django.views.generic import TemplateView

# Заготовки под вьюхи.


class MainPageView(TemplateView):
    template_name: str = "mainapp/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "mainapp/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "mainapp/about.html"


class JobsListingView(TemplateView):
    template_name: str = "mainapp/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "mainapp/job_details.html"
