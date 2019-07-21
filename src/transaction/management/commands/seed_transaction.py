from django_seed import Seed
from django.utils.crypto import get_random_string

from django.core.management.base import BaseCommand

from wallet.models import Wallet
from transaction.models import Transaction

class Command(BaseCommand):
    help = 'Generates 1 object for each app model.'
    help += '\nExample^:./manage.py seed_transaction 12 10'

    def add_arguments(self, parser):
        parser.add_argument('wallet_pk', type=int)
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        amount = options['amount'] if  options['amount'] else 1

        if options['wallet_pk']:
            # try to get user from argument
            try:
                wallet = Wallet.objects.get(pk=options['wallet_pk'])
            except Wallet.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f'Wallet not found: {options["wallet_pk"]}'
                ))
                return None
        else:
            return None


        seeder = Seed.seeder()
        for i in range(0, amount):
            seeder.add_entity(Transaction, 1, {
                'wallet': wallet,
                'address_from': get_random_string(30, '0123456789'),
                'address_to': get_random_string(30, '0123456789'),
                'committed': seeder.faker.date_time_between(
                    start_date="-80d", end_date="now"
                )
            })

        try:
            pks = seeder.execute()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully create objects.')
            )
            self.stdout.write(f"{pks}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
