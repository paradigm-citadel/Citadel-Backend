import datetime as dt


def make_consistent(orig_list, delta, max_value=None, target='datetimefield'):
    """ Fill empty values with previous field
    Example: 1,2,3,6,8 -> 1,2,3,3,3,6,6,8

    :param orig_list: list of dicts
    :param delta: float - difference between values of target field in seconds
    :param max_value: datetime - max datetime to spread data
    :param target: string - name of target field
    :return: (object, flag_appended)
    """
    if not orig_list:
        return

    prev = orig_list[0]

    for i in orig_list:
        while abs(prev[target]-i[target]).total_seconds() / delta > 1:
            if prev[target] > i[target]:
                prev[target] -= dt.timedelta(seconds=delta)
            else:
                prev[target] += dt.timedelta(seconds=delta)

            yield prev, True

        prev = i
        yield i, False

    # append new elements at the end until reach max value
    while max_value and abs(prev[target] - max_value).total_seconds()/delta > 1:
        if prev[target] > max_value:
            prev[target] -= dt.timedelta(seconds=delta)
        else:
            prev[target] += dt.timedelta(seconds=delta)

        yield prev, True
