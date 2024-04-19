from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def simplified_timesince(value):
    """
    Simplifies the timesince to only show the most significant unit.
    """
    if value:
        return timesince(value).split(",")[0]
    else:
        return ""

@register.filter
def like_ratio(likes, dislikes):
    likes, dislikes = int(likes), int(dislikes)
    
    if likes and dislikes:
        return int( ( (likes - dislikes) / (likes + dislikes) ) * 100 )
    
    if not dislikes and likes:
        return 100
    
    if dislikes and not likes:
        return 0
    
    if not dislikes and not likes:
        return 0