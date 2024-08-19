#!/bin/bash

python manage.py makemigrations
python manage.py migrate --fake-initial
python manage.py migrate
python manage.py create_superuser
python manage.py create_staffuser
python manage.py create_group
python manage.py collectstatic --no-input

gunicorn app.wsgi:application --bind 0:8000

