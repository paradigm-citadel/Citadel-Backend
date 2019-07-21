from datetime import datetime

from inflection import underscore
from rest_framework import serializers

from django.db import transaction as dj_transaction
from django.utils import timezone

from transaction.models import Transaction

class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        timestamp = int(str(data)[:10]) # get too big number from API
        return timezone.make_aware(datetime.utcfromtimestamp(timestamp))

class TransactionSerializer(serializers.Serializer):
    tr_hash =  serializers.CharField(max_length=100) # renamed in AddressSerializer __init__
    date = TimestampField()
    value = serializers.FloatField()
    address_from = serializers.CharField(max_length=100, allow_null=True) # renamed in AddressSerializer __init__
    to = serializers.CharField(max_length=100, allow_null=True)
    fee = serializers.FloatField()
    tr_type = serializers.ChoiceField(choices=[i[0] for i in Transaction.MISSIONS]) # renamed in AddressSerializer __init__
    comment = serializers.CharField(max_length=100, required=False, allow_null=True, default='')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
    created = TimestampField(allow_null=True)
    updated = TimestampField(allow_null=True)
    comment = serializers.CharField(max_length=100, required=False)
    transactions = TransactionSerializer(many=True)

    def __init__(self, **kwargs):
        """ Hook for renaming python-reserved keywords """
        for transaction in kwargs['data']['transactions']:
            transaction['tr_hash'] = transaction['hash']
            transaction['address_from'] = transaction['from']
            transaction['tr_type'] = transaction['type']
        super(AddressSerializer, self).__init__(**kwargs)

    def create(self, validated_data):
        raise NotImplementedError('wallet could not be created by API.')

    def update(self, wallet, validated_data):
        wallet.created = validated_data.get('created', None)
        wallet.updated = timezone.now()
        wallet.updated_from_2nd_svr = validated_data.get('updated', None)
        wallet.save()

        if 'transactions' not in validated_data:
            time_str = timezone.now().strftime('%Y:%m:%d %H:%M:%S')
            wallet.transactions_detail = f"{time_str} CHECK:" \
                f" No new transactions"
            wallet.save()
            return wallet

        with dj_transaction.atomic():
            for transaction_data in validated_data['transactions']:
                transaction_dict = dict(transaction_data)

                # Check for existing
                amount = Transaction.objects.filter(
                    wallet=wallet,
                    tr_hash=transaction_dict['tr_hash']
                ).count()
                if amount:
                    continue

                Transaction.objects.create(
                    wallet=wallet,
                    tr_hash=transaction_dict['tr_hash'],
                    address_from=transaction_dict['address_from'],
                    address_to=transaction_dict['to'],
                    mission=underscore(transaction_dict['tr_type']),  # ToDo: убрать underscore, когда 2dbackend исправит # NoQa
                    volume=transaction_dict['value'],
                    commission=transaction_dict['fee'],
                    committed=transaction_dict['date'],
                    comment=transaction_dict['comment']
                )
        time_str = timezone.now().strftime('%Y:%m:%d %H:%M:%S')
        wallet.transactions_detail = f"{time_str} SUCCESS:" \
            f" {len(validated_data['transactions'])} transaction loaded"
        wallet.save()

        return wallet
