#!/bin/bash

sleep 5
sed -i 's/from collections import Callable/from typing import Callable/g' /usr/local/lib/python3.10/collections/__init__.py

if [ "$DEBUG"==True ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata fixtures/goods/*.json
    python manage.py create_superuser
    python manage.py collectstatic --no-input
fi

gunicorn home.wsgi:application --bind 0:8000