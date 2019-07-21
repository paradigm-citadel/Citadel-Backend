import os
import requests

from django.conf import settings
from django.utils import timezone

from wallet.models import Currency, Rate


def request_rates(currency_codes, rate_to_codes):
    """ Execute request to service with rate """
    path = f"data/pricemulti"
    r = requests.get(
        os.path.join(settings.CURRENCY_RATE_SOURCE_URL, path),
        params={
            'fsyms': ','.join([s.upper() for s in currency_codes]),
            'tsyms': ','.join([s.upper() for s in rate_to_codes]),
            'api_key': settings.CURRENCY_RATE_API_KEY
        }
    )
    if r.status_code != 200:
        print(f'Error: {r.text}')
        return None

    response = r.json()
    return response

def handle():
    currencies = Currency.objects.all()
    currencies_codes = [c.code for c in currencies]

    response = request_rates(currencies_codes, ('USD', 'BTC'))
    if not response:
        return None

    for c in currencies:
        rate = response.get(c.code, None)
        if not rate:
            continue

        Rate.objects.create(
            currency=c,
            datetime=timezone.now(),
            usd=rate.get('USD', None),
            btc=rate.get('BTC', None)
        )

    print(f'Successfully upload rate history for {currencies}.')
