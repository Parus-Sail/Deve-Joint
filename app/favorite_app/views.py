from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views import View
from favorite_app.models import FavoriteProjects
from project_app.models import Project


class FavoriteProjectsView(LoginRequiredMixin, View):
    template_name = "favorite_app/favorites.html"

    def get(self, request):
        title = "favorite projects"
        favorite_projects_items = FavoriteProjects.objects.filter(user=request.user)
        context = {
            "title": title,
            "favorite_projects_items": favorite_projects_items,
        }
        return render(request, self.template_name, context)


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
