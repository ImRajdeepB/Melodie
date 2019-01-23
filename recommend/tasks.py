import csv
import pandas as pd
from sklearn.model_selection import train_test_split

from .models import AppUser, Listen
from . import recommender

from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab(minute='*/1')), name="manipulate", ignore_result=True)
def manipulate():
    with open('t.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['user_id', 'song_id', 'listen_count',
                         'title', 'release', 'artist_name', 'song', 'year'])
        for l in Listen.objects.all():
            if l.app_user.count() == 1:
                writer.writerow([l.app_user.values().get()['id'], l.container.id, l.listen_count, l.container.title, l.container.release_by,
                                 l.container.artist_name, (l.container.title + ' - ' + l.container.artist_name), l.container.year])
            elif l.app_user.count() > 1:
                for au in l.app_user.all():
                    writer.writerow([au.id, l.container.id, l.listen_count, l.container.title, l.container.release_by,
                                     l.container.artist_name, (l.container.title + ' - ' + l.container.artist_name), l.container.year])
            elif l.app_user.count() == 0:
                writer.writerow(['None', l.container.id, l.listen_count, l.container.title, l.container.release_by,
                                 l.container.artist_name, (l.container.title + ' - ' + l.container.artist_name), l.container.year])

    song_df = pd.read_csv('t.csv')
    aggregation_functions = {'listen_count': 'sum', 'song': 'first'}
    song_grouped = song_df.groupby(song_df['song_id']).aggregate(
        aggregation_functions).reset_index()
    grouped_sum = song_grouped['listen_count'].sum()
    song_grouped['percentage'] = song_grouped['listen_count'].div(
        grouped_sum)*100
    song_grouped.sort_values(['listen_count', 'song'],
                             ascending=[0, 1]).reset_index()

    users = song_df['user_id'].unique()
    songs = song_df['song'].unique()

    train_data, test_data = train_test_split(
        song_df, test_size=0.20, random_state=0)

    pm = recommender.popularity_recommender_py()
    pm.create(train_data, 'user_id', 'song')

    is_model = recommender.item_similarity_recommender_py()
    is_model.create(train_data, 'user_id', 'song')
