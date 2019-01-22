from django.urls import path
from .views import HomeView, AppUserFormView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', AppUserFormView.as_view(), name='signup'),
]
