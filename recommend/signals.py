from django.dispatch import receiver
# from django.core.signals import post_save
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import AppUser


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        AppUser.objects.get_or_create(user=kwargs.get('instance'))
