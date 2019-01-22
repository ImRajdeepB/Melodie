from django.contrib import admin
from .models import AppUser, Song, Listen, Album

admin.site.register(AppUser)
admin.site.register(Song)
admin.site.register(Listen)
admin.site.register(Album)
