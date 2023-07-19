from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views import View
from favorite_app.models import FavoriteProjects, FavoriteVacancies
from project_app.models import Project
from vacancy_app.models import Vacancy


class FavoritesView(LoginRequiredMixin, View):
    template_name = "favorite_app/favorites.html"

    def get(self, request):
        projects_title = "favorite projects"
        projects_items = FavoriteProjects.objects.filter(user=request.user)
        vacancies_title = "favorite vacancies"
        vacancies_items = FavoriteVacancies.objects.filter(user=request.user)
        context = {
            "projects_title": projects_title,
            "projects_items": projects_items,
            "vacancies_title": vacancies_title,
            "vacancies_items": vacancies_items,
        }
        return render(request, "favorite_app/favorites.html", context)


class FavoriteProjectsAdd(LoginRequiredMixin, View):

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        favorites = FavoriteProjects.objects.filter(user=request.user, project=project).first()
        if not favorites:
            favorites = FavoriteProjects(user=request.user, project=project)
        favorites.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FavoriteProjectsRemove(LoginRequiredMixin, View):

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        favorites_pk = FavoriteProjects.objects.filter(user=request.user, project=project).first().pk
        favorites_record = get_object_or_404(FavoriteProjects, pk=favorites_pk)
        favorites_record.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FavoriteVacanciesAdd(LoginRequiredMixin, View):

    def get(self, request, pk):
        vacancy = get_object_or_404(Vacancy, pk=pk)
        favorites = FavoriteVacancies.objects.filter(user=request.user, vacancy=vacancy).first()
        if not favorites:
            favorites = FavoriteVacancies(user=request.user, vacancy=vacancy)
        favorites.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FavoriteVacanciesRemove(LoginRequiredMixin, View):

    def get(self, request, pk):
        vacancy = get_object_or_404(Vacancy, pk=pk)
        favorites_pk = FavoriteVacancies.objects.filter(user=request.user, vacancy=vacancy).first().pk
        favorites_record = get_object_or_404(FavoriteVacancies, pk=favorites_pk)
        favorites_record.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
