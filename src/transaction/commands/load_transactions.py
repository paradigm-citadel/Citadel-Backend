from rest_framework.exceptions import APIException

from wallet.models import Wallet
from second_backend.serializers import AddressSerializer
from second_backend.endpoints import get_address


def handle(wallet_pk):
    wallet = Wallet.objects.get(pk=wallet_pk)

    address = get_address(wallet.currency.net, wallet.address)
    if not address:
        raise APIException('Невозможно получить ответ от second_backend (get_address)')

    serializer = AddressSerializer(instance=wallet, data=address)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    wallet.initialized = True
    wallet.save()

