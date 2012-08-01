from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_points(points, completed=True, autoescape=None):
    if completed:
        style = 'success' if points > 0 else 'important'
        title = 'Points received'
    else:
        style = 'warning'
        title = 'Points for correct prediction'
    if autoescape:
        points = conditional_escape(points)
    return mark_safe('<span class="badge badge-{style}" title="{title}">'
            '{points}</span>'.format(style=style, points=points, title=title))
display_points.needs_autoescape = True
