from config import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class StaffRequiredMixin(object):
    """
    Проверяем что пользователь is_staff, иначе redirect to settings.LOGIN_URL
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


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
