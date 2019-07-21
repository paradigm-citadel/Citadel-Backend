import os
import requests
from datetime import datetime

from django.db.models import Min
from django.conf import settings
from django.utils.timezone import make_aware

from wallet.models import Currency, Rate

STEP = 2000

def request_rates(currency_code, start_ts, rate_to):
    """ Execute request to service with rate """
    path = f"data/histoday"
    r = requests.get(
        os.path.join(settings.CURRENCY_RATE_SOURCE_URL, path),
        params={
            'fsym': currency_code,
            'tsym': rate_to,
            'limit': STEP,
            'toTs': int(start_ts),
            'api_key': settings.CURRENCY_RATE_API_KEY
        }
    )
    if r.status_code != 200:
        print(f'Error: {r.text}')
        return None

    response = r.json()
    if not response.get('Response', None):
        print(f'Error: {r.text}')
        return None

    return response

def load_history(currency, usd):
    """ Upload and save rate history for currencies """
    query = Rate.objects.filter(currency=currency)
    if usd:
        rate_to = 'USD'
        query = query.filter(usd__isnull=False)
    else:
        rate_to = 'BTC'
        query = query.filter(btc__isnull=False)
    query = query.aggregate(
        min=Min('datetime')
    )
    min_date = query['min'] if query['min'] else datetime.now()
    finish_ts = min_date.timestamp()
    last_ts = finish_ts

    # 1230768000 = 2009-01-01
    while last_ts > 1230768000:
        date_str = datetime.utcfromtimestamp(
            finish_ts
        ).strftime('%Y-%m-%d %H:%M:%S')
        print(
            f"Load last {STEP} {currency.code}-{rate_to} to {date_str}"
        )

        usd_rates = request_rates(
            currency.code.upper(), finish_ts, rate_to)

        if not usd_rates or not usd_rates.get('TimeFrom', None):
            print(f'Something went wrong')
            break

        for day_rate in usd_rates['Data']:
            date_str = datetime.utcfromtimestamp(
                day_rate['time']
            ).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\rCurrent date {date_str}", end='\r')

            # Service returns zeros if no data available
            if day_rate['low'] + day_rate['high'] == 0:
                continue

            rate, created = Rate.objects.get_or_create(
                currency=currency,
                datetime=make_aware(
                    datetime.utcfromtimestamp(day_rate['time'])
                )
            )

            if usd:
                rate.usd = (day_rate['low'] + day_rate['high']) / 2
            else:
                rate.btc = (day_rate['low'] + day_rate['high']) / 2
            rate.save()

        last_ts = finish_ts
        finish_ts = usd_rates['TimeFrom']


def handle(currency_pk):
    currency = Currency.objects.get(pk=currency_pk)

    load_history(currency, usd=True)
    load_history(currency, usd=False)
    currency.initialized = True
    currency.save()

    print(f'Successfully upload rate history for {currency.code}.')
