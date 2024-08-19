#!/bin/bash

sleep 15
python manage.py makemigrations tasks
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py create_superuser
python manage.py load_data

gunicorn app.wsgi:application --bind 0:8000

