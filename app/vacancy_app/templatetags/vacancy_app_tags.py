from calendar import monthrange
from datetime import datetime, timedelta, timezone
from math import trunc

from django import template

register = template.Library()


@register.inclusion_tag('tags/user_date_time.html')
def get_user_date_time(utc_date_time):
    context = {
        'utc_date_time': utc_date_time,
    }
    return context


@register.inclusion_tag('tags/user_date.html')
def get_user_date(utc_date_time):
    context = {
        'utc_date_time': utc_date_time,
    }
    return context


@register.filter()
def date_diff(utc_date_time):

    def month_delta(d1, d2):
        delta = 0
        while True:
            mdays = monthrange(d1.year, d1.month)[1]
            d1 += timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
        return delta

    now = datetime.now(timezone.utc)
    time_delta = now - utc_date_time
    minutes = trunc(time_delta.total_seconds() / 60)
    hours = trunc(time_delta.total_seconds() / 60 / 60)
    days = time_delta.days
    months = month_delta(utc_date_time, now)
    years = trunc(months / 12)
    if years > 0:
        answer = [years, 'year']
    elif months > 0:
        answer = [months, 'month']
    elif days > 0:
        answer = [days, 'day']
    elif hours > 0:
        answer = [hours, 'hour']
    elif minutes >= 1:
        answer = [minutes, 'minute']
    else:
        return 'now'
    if answer[0] > 1:
        answer[1] += 's'
    return f'{answer[0]} {answer[1]} ago'
