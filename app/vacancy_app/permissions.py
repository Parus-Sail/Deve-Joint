from config import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class OwnerRequiredMixin(object):
    """ Mixin which check user is owner of object """

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.owner != request.user:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(object):
    """
    Проверяем что пользователь is_staff, иначе redirect to settings.LOGIN_URL
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
