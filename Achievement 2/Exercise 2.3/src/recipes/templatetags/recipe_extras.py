from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get item from dictionary/pandas Series"""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key, '')
    return getattr(dictionary, key, '')

