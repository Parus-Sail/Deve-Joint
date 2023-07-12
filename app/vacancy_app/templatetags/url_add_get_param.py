from django import template
from django.utils.http import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_add_get_param(context, **kwargs):
    """
    Добавляем в шаблон get параметры
    """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
