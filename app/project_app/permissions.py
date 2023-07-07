from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(object):
    """ Mixin which check user is owner of project """

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# создать группу project_owner с помощью метода create()
# project_owner_group = Group.objects.create(name="project_owner")
# project_admin_group = Group.objects.create(name="project_admin")
# project_member_group = Group.objects.create(name="project_member")
