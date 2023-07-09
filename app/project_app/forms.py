from auth_app.utils import DivErrorList  # todo может вынести в отдельный блок?
from django import forms

from . import models


class ProjectCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ("title", "description")
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # убираем стандартную помощь от Django
            self.fields[field].help_text = None
        # кастомный css для ошибок
        self.error_class = DivErrorList

    class Meta:
        model = models.Project
        fields = ("title", "description")


class ProjectUpdateForm(ProjectCreateForm):
    ...
