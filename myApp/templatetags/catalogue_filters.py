from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Split a string by the given argument"""
    if value:
        return [item.strip() for item in value.split(arg) if item.strip()]
    return []

@register.filter(name='trim')
def trim(value):
    """Trim whitespace from a string"""
    if value:
        return str(value).strip()
    return value

