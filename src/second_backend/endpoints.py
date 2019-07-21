import json
import os

import requests
from django.conf import settings
from django.utils import timezone

DEFAULT_DATE_FROM = timezone.datetime(year=2009, month=1, day=1)
DEFAULT_DATE_TO = timezone.now()

DEFAULT_TIMEOUT = 5  # seconds


# ToDo: обернуть вызовы аналогично https://github.com/junto-team/Nyyak-Backend-Main/blob/master/src/common/utils/services.py # NoQa
def get_address(net_code, address, date_from=DEFAULT_DATE_FROM, date_to=DEFAULT_DATE_TO):
    path = f"net/{net_code}/address/{address}"
    r = requests.get(os.path.join(settings.SECOND_BACKEND_URL, path), params={
        date_from: date_from,
        date_to: date_to
    })
    if r.status_code != 200:
        return None

    return json.loads(r.text)


def delete_address(net_code, address):
    path = f"net/{net_code}/address/{address}"
    r = requests.delete(os.path.join(settings.SECOND_BACKEND_URL, path))
    if r.status_code != 200:
        return None

    return json.loads(r.text)


def get_polls(limit=None, offset=None, is_active=None):
    path = "net/voting"

    if is_active is True:
        is_active = 'true'
    elif is_active is False:
        is_active = 'false'

    params = {
        'limit': limit,
        'offset': offset,
    }

    if is_active is not None:
        params['is_active'] = is_active

    try:
        r = requests.get(os.path.join(settings.SECOND_BACKEND_URL, path), params=params, timeout=DEFAULT_TIMEOUT)
    except:
        return None

    if r.status_code != 200:
        return None

    return json.loads(r.text)


def get_currencies_statistics():
    path = "net/info"
    r = requests.get(os.path.join(settings.SECOND_BACKEND_URL, path))
    if r.status_code != 200:
        return None

    return json.loads(r.text)
