from datetime import datetime

from django.db import transaction
from django.utils import timezone

from Citadel.celery import app
from second_backend.endpoints import get_currencies_statistics
from wallet.models import Wallet, Currency, CurrencyStatistics
from transaction.commands import load_transactions, update_transactions
from wallet.commands import load_rate, update_rate


@app.task
def update_wallets():
    for wallet in Wallet.objects.all():
        try:
            if wallet.initialized:
                update_transactions.handle(wallet.pk)
            else:
                load_transactions.handle(wallet.pk)
        except Exception as e:
            time_str = timezone.now().strftime('%Y:%m:%d %H:%M:%S')
            wallet.transactions_detail = f"{time_str} ERROR: " \
                f"exception on Celery task {e}"
            wallet.save()


@app.task
def update_rates():
    for currency in Currency.objects.all():
        if not currency.initialized:
            load_rate.handle(currency.pk)
    update_rate.handle()


@app.task
def update_currency_statistics():
    statistics = get_currencies_statistics()

    if not statistics:
        # ToDo: залоггировать
        return

    currencies = list(Currency.objects.all())

    with transaction.atomic():
        for currency in currencies:
            statistics_data = [
                data for data in statistics
                if data['net'].lower() == currency.net.lower()
            ]

            if not statistics_data:
                # ToDo: залоггировать
                continue

            statistics_data = statistics_data[0]

            data = {
                'price_usd': statistics_data['priceUsd'],
                'price_btc': statistics_data['priceBtc'],
                'price_usd_delta_24': statistics_data['priceUsdDelta24'],
                'price_btc_delta_24': statistics_data['priceBtcDelta24'],
                'yielded': statistics_data['yield'],
                'market_cap': statistics_data['marketCap'],
                'circulating_supply': statistics_data['circulatingSupply'],
                'staking_rate': statistics_data['stakingRate'],
                'unbonding_period': statistics_data['unbondingPeriod'],
                'second_backend_update_datetime': datetime.utcfromtimestamp(
                    int(str(statistics_data['updatedAt'])[:10])
                ),
            }

            if getattr(currency, 'statistics', None):
                CurrencyStatistics.objects.filter(currency=currency).update(**data)
            else:
                CurrencyStatistics.objects.create(**data, currency=currency)
