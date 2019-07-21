from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from wallet.filters import CurrencyFilter
from wallet.models.currency import Currency

from wallet.serializers.currency import CurrencySerializer


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.init_currencies.select_related('statistics').prefetch_related('social')
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated, ]
    filter_class = CurrencyFilter
