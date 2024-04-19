from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def simplified_timesince(value):
    if value:
        return timesince(value).split(",")[0]
    else:
        return ""