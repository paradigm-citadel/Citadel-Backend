from django.db.models import Min, Max

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from wallet.serializers.currency import CurrencySerializer

from Citadel.helpers import get_new_color
from wallet.models.wallet import Wallet
from transaction.models.transaction import Transaction


class WalletSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    chart_date_from = serializers.SerializerMethodField()
    chart_date_to = serializers.SerializerMethodField()

    def get_chart_date_from(self, wallet):
        return Transaction.objects.filter(
            wallet=wallet
        ).aggregate(
            min=Min('committed')
        ).get('min', None)

    def get_chart_date_to(self, wallet):
        return Transaction.objects.filter(
            wallet=wallet
        ).aggregate(
            max=Max('committed')
        ).get('max', None)

    class Meta:
        model = Wallet
        fields = (
            'pk',
            'initialized',
            'currency',
            'address',
            'color',
            'created',
            'updated',
            'chart_date_from',
            'chart_date_to'
        )

class WalletEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            'pk',
            'currency',
            'address'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Wallet.objects.all(),
                fields=('currency', 'address')
            )
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        wallet = super(WalletEditSerializer, self).create(validated_data)
        exists_colors = Wallet.objects.filter(
            user=wallet.user
        ).values_list('color', flat=True)
        wallet.color = get_new_color(exclude=exists_colors)
        wallet.save()

        return wallet