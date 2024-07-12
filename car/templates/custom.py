from django import template

register = template.Library()

@register.filter
def number_to_letter(value):
    letters = 'ABCD'
    try:
        return letters[int(value) - 1]
    except (ValueError, IndexError):
        return ''