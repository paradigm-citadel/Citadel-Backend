from django.core.management.base import BaseCommand

from wallet.commands import update_rate


class Command(BaseCommand):
    help = 'Loads rate history for currency.'

    def handle(self, *args, **options):
        update_rate.handle()
