from django.shortcuts import render
from django.views import View, generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


from .models import AppUser, Song, Listen, Album
from .forms import AppUserForm
from .tasks import manipulate
from . import recommender


@login_required(login_url='/login')
def home(request):
    if request.user.is_authenticated:
        songs = Song.objects.all()
        albums = Album.objects.all()
        context = {'albums': albums, 'songs': songs}
        uid = request.user.id
        print(request.user.id)
        pm = None
        pm = manipulate(pm)
        rec = pm.recommend(uid)
        print(rec)
        return render(request, 'recommend/index.html', context=context)
    else:
        return render(request, '/templates/registration/login.html')


# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return HttpResponseRedirect('/')
#     else:
#         # Return an 'invalid login' error message.
#         return HttpResponse('invalid')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'recommend/signup.html'


# class HomeView(TemplateView):
#     template_name = 'recommend/index.html'


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
