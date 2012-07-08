from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def user_prediction_match_points(user, prediction):
    points = 0
    for user_prediction in prediction.userprediction_set.filter(user=user):
        for choice in user_prediction.userpredictionchoice_set.all():
            if choice.event_contestant in prediction.matches.all():
                points += prediction.points
    return points

@register.filter
def user_team_match_points(user, prediction):
    points = 0
    if prediction.can_match_team:
        for contestant in user.team_set.all()[0].contestants.all():
            if contestant in prediction.contestants:
                points += prediction.points / 2
    return points


@register.filter
def display_points(points, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda p: p
    style = 'success' if points > 0 else 'important'
    return mark_safe('<span class="badge badge-{style}">{points}</span>'.format(
            style=style, points=esc(points)))
display_points.needs_autoescape = True
