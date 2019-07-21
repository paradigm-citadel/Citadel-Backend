from django.core.management.base import BaseCommand

from Citadel.helpers import get_new_color
from wallet.models import Wallet


class Command(BaseCommand):
    help = 'Loads rate history for currency.'

    def handle(self, *args, **options):
        for wallet in Wallet.objects.filter(color__isnull=True):
            exists_colors = Wallet.objects.filter(
                user=wallet.user
            ).values_list('color', flat=True)
            wallet.color = get_new_color(exclude=exists_colors)
            wallet.save()
