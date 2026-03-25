#!/bin/sh
set -e

python config/db_wait.py
python manage.py migrate --noinput
python manage.py seed_demo
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
