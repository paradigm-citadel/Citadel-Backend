#!/bin/bash

./manage.py migrate

gunicorn -c /config/gunicorn/gunicorn-prod.py Citadel.wsgi:application