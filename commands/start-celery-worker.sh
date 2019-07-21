#!/bin/bash

celery -A Citadel.celery worker
