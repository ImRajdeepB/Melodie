from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        return self.user.username
