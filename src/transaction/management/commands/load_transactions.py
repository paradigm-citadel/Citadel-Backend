from django.core.management.base import BaseCommand

from transaction.commands import load_transactions

class Command(BaseCommand):
    help = 'Upload all transactions for wallets'
    help += '\nExample^:./manage.py load_transactions 12 '

    def add_arguments(self, parser):
        parser.add_argument('wallet_pk', type=int)

    def handle(self, *args, **options):
        load_transactions.handle(options['wallet_pk'])
