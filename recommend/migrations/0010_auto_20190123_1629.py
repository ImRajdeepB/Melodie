# Generated by Django 2.1.5 on 2019-01-23 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0009_song_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(default='', upload_to='albums'),
        ),
    ]