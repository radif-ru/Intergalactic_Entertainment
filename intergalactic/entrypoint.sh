#!/bin/bash

python manage.py collectstatic --no-input --clear

gunicorn intergalactic.wsgi:application -b 0.0.0.0:8000 --reload
