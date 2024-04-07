from django import template

from config import settings

register = template.Library()


@register.filter
def cut(value):
    return f'{value[:100]}...'
