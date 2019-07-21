#!/bin/bash

rm -f '/tmp/Citadel.pid'
celery -A Citadel.celery beat --pidfile=/tmp/Citadel.pid -s /var/celerybeat-schedule
