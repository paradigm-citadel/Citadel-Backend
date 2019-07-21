from django.core.management.base import BaseCommand

from wallet.commands import load_rate


class Command(BaseCommand):
    help = 'Loads rate history for currency.'

    def add_arguments(self, parser):
        parser.add_argument('currency_pk', type=int)

    def handle(self, *args, **options):
        load_rate.handle(options['currency_pk'])
