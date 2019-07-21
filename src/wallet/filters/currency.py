from django_filters.rest_framework import FilterSet

from Citadel.helpers.filters import ListFilter
from wallet.models import Currency


class CurrencyFilter(FilterSet):
    net = ListFilter(field_name='net')

    class Meta:
        model = Currency
        fields = ['net']
