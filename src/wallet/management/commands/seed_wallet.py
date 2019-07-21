from django.contrib.auth import get_user_model
from django_seed import Seed

from django.core.management.base import BaseCommand

from wallet.models import Wallet, Currency, Rate


User = get_user_model()


class Command(BaseCommand):
    help = 'Generates 1 object for each app model.'

    def add_arguments(self, parser):
        parser.add_argument('user_pk', type=int, nargs='*')

    def handle(self, *args, **options):
        amount = 1

        if options['user_pk']:
            # try to get user from argument
            try:
                user = User.objects.get(pk=options['user_pk'])
            except User.DoesNotExist as e:
                self.stderr.write(self.style.ERROR(
                    f'User not found: {options["user"]}'
                ))
                return None
        else:
            user = User.objects.filter(is_staff=True).first()

        seeder = Seed.seeder()
        seeder.add_entity(Currency, amount, {
            'name': seeder.faker.cryptocurrency_name(),
            'code': seeder.faker.cryptocurrency_code()
        })
        seeder.add_entity(Wallet, amount, {
            'user': user,
        })
        seeder.add_entity(Rate, amount)

        try:
            pks = seeder.execute()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully create objects.')
            )
            self.stdout.write(f"{pks}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
