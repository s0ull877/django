#!/bin/bash

sleep 5
if [ $DEBUG==True ]; then
    python manage.py makemigrations
    python manage.py migrate --fake-initial
    python manage.py migrate
    python manage.py loaddata fixtures/tree_menu/categories.json
    python manage.py loaddata fixtures/tree_menu/subcategories.json
    python manage.py create_superuser
    python manage.py collectstatic --no-input
fi

gunicorn app.wsgi:application --bind 0:8000
