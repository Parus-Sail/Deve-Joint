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
