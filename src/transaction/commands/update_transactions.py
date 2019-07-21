from django.db.models import Max
from django.utils import timezone

from wallet.models import Wallet
from second_backend.serializers import AddressSerializer
from second_backend.endpoints import get_address


def handle(wallet_pk):
    wallet = Wallet.objects.get(pk=wallet_pk)
    max_date = wallet.transactions.all().aggregate(
        max=Max('committed')
    ).get('max', None)
    if max_date:
        max_date = max_date.timestamp()
    else:
        max_date = timezone.datetime(year=2009, month=1, day=1).timestamp()

    address = get_address(wallet.currency.net, wallet.address, max_date)
    serializer = AddressSerializer(instance=wallet, data=address)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
