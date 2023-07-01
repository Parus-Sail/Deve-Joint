from django.views.generic import TemplateView

# Заготовки под вьюхи.


class MainPageView(TemplateView):
    template_name: str = "main_app/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "main_app/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "main_app/about.html"


class JobsListingView(TemplateView):
    template_name: str = "main_app/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "main_app/job_details.html"
