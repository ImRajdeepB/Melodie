from django import forms
from django.contrib.auth.models import User
from .models import AppUser, Song, Listen, Album


class AppUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('email',)
