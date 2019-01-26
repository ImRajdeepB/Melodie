# Melodie

### Getting started
Install a virtual environment on [mac/linux](https://www.codingforentrepreneurs.com/blog/install-django-on-mac-or-linux/) or [windows](https://www.codingforentrepreneurs.com/blog/install-python-django-on-windows)
```
$ pip install -r requirements.txt
```
Fire up Redis:
```
$ redis-server
```
Open 2 other terminal windows and run:
```
$ celery -A melodie worker -l info
$ celery -A melodie beat -l info
```
Set up Django in a different window:
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```