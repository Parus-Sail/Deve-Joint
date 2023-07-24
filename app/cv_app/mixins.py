from favorite_app.models import FavoriteCVs


class FavoriteCVsMixin:
    """ Добавляет в контекст список pk избранных резюме """

    def get_context_data(self, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        favorites_of_user = FavoriteCVs.objects.filter(user=self.request.user.id)
        favorites_pk_list = [item.cv.pk for item in favorites_of_user]
        context["favorites_pk_list"] = favorites_pk_list
        return context
