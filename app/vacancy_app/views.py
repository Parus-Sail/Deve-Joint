from django.views.generic import TemplateView


class JobsListingView(TemplateView):
    template_name: str = "vacancy_app/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "vacancy_app/job_details.html"
