from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import AppUser, Song, Listen, Album
from .forms import AppUserForm


class HomeView(TemplateView):
    template_name = 'recommend/index.html'


class AppUserFormView(View):
    form_class = AppUserForm
    initial = {'key': 'value'}
    template_name = 'recommend/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})
