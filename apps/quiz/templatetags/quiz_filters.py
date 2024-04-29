from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]