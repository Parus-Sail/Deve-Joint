from django import forms
from django.contrib.auth import get_user

from . import models


class CVCreationForm(forms.ModelForm):

    class Meta:
        model = models.CV
        exclude = ['owner', 'created', 'updated']
