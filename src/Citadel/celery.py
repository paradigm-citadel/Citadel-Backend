import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Citadel.settings')

app = Celery('citadel', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['wallet'])

app.conf.beat_schedule = {
    'check_transactions': {
        'task': 'wallet.tasks.update_wallets',
        'schedule': 60.0  # run task every 60 seconds
    },
    'check_rates': {
        'task': 'wallet.tasks.update_rates',
        'schedule': 60.0 * 30  # run task every 30 minutes
    },
    'update_currency_statistics': {
        'task': 'wallet.tasks.update_currency_statistics',
        'schedule': 60.0 * 10 # run task every 10 minutes
    }
}
