from favorite_app.models import FavoriteVacancies


class RequestFormKwargsMixin:
    """
    Передаем request в форму.
    CBV mixin which puts the request into the form kwargs.
    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargsMixin, self).get_form_kwargs()

        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs


class FavoritesMixin:
    """ Добавляет в контекст список pk избранных вакансий """

    def get_context_data(self, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        favorites_of_user = FavoriteVacancies.objects.filter(user=self.request.user.id)
        favorites_pk_list = [item.vacancy.pk for item in favorites_of_user]
        context["favorites_pk_list"] = favorites_pk_list
        return context
