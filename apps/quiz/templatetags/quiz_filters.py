import os

from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter(name='file_exists')
def file_exists(file_path):
    return os.path.exists(file_path)