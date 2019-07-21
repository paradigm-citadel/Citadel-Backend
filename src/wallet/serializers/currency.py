from rest_framework import serializers

from wallet.models.currency import Currency, CurrencySocial, CurrencyStatistics


class CurrencySocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencySocial
        fields = (
            'pk',
            'name',
            'url',
            'icon',
        )


class CurrencyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyStatistics
        fields = (
            'pk',
            'currency',
            'price_usd',
            'price_btc',
            'price_usd_delta_24',
            'price_btc_delta_24',
            'yielded',
            'market_cap',
            'circulating_supply',
            'staking_rate',
            'unbonding_period',
            'second_backend_update_datetime',
            'update_datetime',
        )


class CurrencySerializer(serializers.ModelSerializer):
    statistics = CurrencyStatisticsSerializer()
    social = CurrencySocialSerializer(many=True)

    class Meta:
        model = Currency
        fields = (
            'pk',
            'sign',
            'name',
            'description',
            'code',
            'icon',
            'social',
            'statistics',
            'net',
        )
