#!/bin/bash

sed -i 's/from collections import/from typing import/g' /usr/local/lib/python3.10/site-packages/celery/utils/text.py

sleep 5
if [ $DEBUG==True ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata products/fixtures/*.json
    python manage.py create_superuser
    python manage.py collectstatic --no-input
fi

gunicorn store.wsgi:application --bind 0:8000
