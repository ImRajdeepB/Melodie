from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='', blank=True)
    # user_id = models.CharField(max_length=50)
    # listens = models.ManyToManyField('Listen')

    def __str__(self):
        return self.user.username


class Song(models.Model):
    song_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    release_by = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=50, default='', blank=True)
    audio_file = models.FileField(upload_to='music')
    # listens = models.IntegerField(default=0, blank=True)
    # listeners = models.ManyToManyField(AppUser, through='Listen')

    def __str__(self):
        return '%s - %s' % (self.title, self.artist_name)


class Listen(models.Model):
    container = models.ForeignKey(
        Song, db_index=True, on_delete=models.CASCADE)
    app_user = models.ManyToManyField(AppUser)
    # song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listen_count = models.IntegerField(default=0)

    def __str__(self):
        return self.container.title + ' - '+self.container.artist_name + ': ' + str(self.listen_count)


class Album(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song)
    genre = models.CharField(max_length=50, default='', blank=True)
    album_logo = models.ImageField(upload_to='albums', default='')

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        AppUser.objects.get_or_create(user=kwargs.get('instance'))
