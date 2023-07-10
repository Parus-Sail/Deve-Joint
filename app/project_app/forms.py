# from auth_app.utils import DivErrorList
# from django import forms

# from . import models

# # todo может вынести в отдельный блок?
# class MixinCssFormClasses:

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         fields = ("title", "description")

#         for field in fields:
#             # кастомный css для полей
#             self.fields[field].widget.attrs.update({"class": "form-control"})
#             # убираем стандартную помощь от Django
#             self.fields[field].help_text = None
#         # кастомный css для ошибок
#         self.error_class = DivErrorList

# class ProjectForm(MixinCssFormClasses, forms.ModelForm):

#     class Meta:
#         model = models.Project
#         fields = ("title", "description")

# class ConfirmDelete(MixinCssFormClasses, forms.ModelForm):

#     class Meta:
#         model = models.Project
#         fields = ("title", "description")
