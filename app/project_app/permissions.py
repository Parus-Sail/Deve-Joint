from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(object):
    """ Mixin which check user is owner of project """

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
