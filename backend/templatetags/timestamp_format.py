from django import template

register = template.Library()

@register.filter
def timestamp_format(value):
    '''
    Converts a int value into mm:ss format.
    '''
    value = int(value)
    minutes = value // 60
    seconds = value % 60
    return f'{minutes:02}:{seconds:02}'