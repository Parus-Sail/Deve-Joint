from django.views.generic import TemplateView

# Заготовки под вьюхи.


class MainPageView(TemplateView):
    template_name: str = "MainPageApp/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "MainPageApp/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "MainPageApp/about.html"


class JobsListingView(TemplateView):
    template_name: str = "MainPageApp/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "MainPageApp/job_details.html"
