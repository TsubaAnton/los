from django import template

from config import settings

register = template.Library()


@register.filter
def mediapath(value):
    print(value)
    """Шаблонный тег для вывода картинки на экран"""
    return f'/media/{value}'
