# Старая реализация. Временно оставил на всякий случай. Фронт попросил переделать по-другому
from django.conf import settings


def _get_scale_based_on_points_required(date_from, date_to, points_required):
    """ Define best datetime scale parameters for required number of points

    :param date_from: first date
    :param date_to: second date
    :param points_required: number of objects that will be returned if
        db groups by scale parameter
    :return: name of closest scale parameter
    """
    if not (date_from and date_to):
        return 'week'

    seconds = abs(date_to - date_from).total_seconds()

    choices_coeffs = {
        'month': 1 / 60 / 60 / 24 / 30.5,
        'week': 1 / 60 / 60 / 24 / 7,
        'day': 1 / 60 / 60 / 24,
        'hour': 1 / 60 / 60,
        'minute': 1 / 60
    }

    choices_distances = {c: abs(points_required - coeff*seconds)
        for c, coeff in choices_coeffs.items()
        if coeff * seconds >= points_required * 0.7
    }

    result = 'day'
    if choices_distances:
        result = min(choices_distances, key=choices_distances.get)
    return result


def _get_scale_based_on_date(date_from, date_to):
    delta = (date_to - date_from).days

    if delta <= 15:
        return 'day'

    if 15 < delta <= 15 * 7:
        return 'week'

    if 15 * 7 < delta <= 15 * 4 * 7:
        return 'month'
    return 'year'


def define_scale(date_from, date_to, add_balance):
    """ Define best datetime scale parameters

    :param date_from: first date
    :param date_to: second date
    :param add_balance: reward/total balance (bool)
    :return: name of closest scale parameter
    """
    if not add_balance:
        return _get_scale_based_on_date(date_from, date_to)
    return _get_scale_based_on_points_required(date_from, date_to, settings.CHART_PRECISION)


def get_second(scale):
    choices_coeffs = {
        'year': 60 * 60 * 24 * 7 * 30.5 * 365,
        'month': 60 * 60 * 24 * 7 * 30.5,
        'week': 60 * 60 * 24 * 7,
        'day': 60 * 60 * 24,
        'hour': 60 * 60,
        'minute': 60
    }
    return choices_coeffs.get(scale, None)
