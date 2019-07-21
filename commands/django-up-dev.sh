#!/bin/bash

./manage.py migrate

gunicorn -c /config/gunicorn/gunicorn-dev.py Citadel.wsgi:application