from rest_framework import serializers

from transaction.models import Transaction
from wallet.models import Rate


class TransactionSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='wallet.currency.code',read_only=True)
    volume_usd = serializers.SerializerMethodField()
    volume_btc = serializers.SerializerMethodField()

    # TODO optimize rate requests
    def get_volume_usd(self, obj):
        return obj.volume * \
               Rate.get_actual_rates(currency=obj.wallet.currency)['usd']

    def get_volume_btc(self, obj):
        return obj.volume * \
               Rate.get_actual_rates(currency=obj.wallet.currency)['btc']

    class Meta:
        model = Transaction
        fields = (
            'pk',
            'wallet',
            'currency',
            'address_from',
            'address_to',
            'mission',
            'volume',
            'volume_usd',
            'volume_btc',
            'commission',
            'committed',
            'comment'
        )
        read_only_fields = (
            'pk',
            'currency'
        )
