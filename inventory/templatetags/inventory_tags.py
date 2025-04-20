from django import template

register = template.Library()

@register.filter
def filter_status(rooms, status):
    return [room for room in rooms if room.status == status]

@register.filter
def subtract(value, arg):
    return value - arg 